import json
import time
import cv2
import sys
from cvzone.HandTrackingModule import HandDetector
import tensorflow as tf
import numpy as np
import pickle
from keras.utils import pad_sequences

#sys.path.append("../Depth")
from Depth.StereoVisionClass import Stereo_Vision
#sys.path.append("../Controller")
from Controller.ControllerClass import ActionController
sys.path.append(".")


class PredictiveClass (object):

    ######## Configuration functions: constructor and Depth ########
    def __init__(self, camera):
        self.in_text_tokenizer = ""
        with open('./Prediction/models&tokenizer/in_tokenizer.pickle', 'rb') as handle:
            self.in_text_tokenizer = pickle.load(handle)

        self.out_text_tokenizer = ''
        with open('./Prediction/models&tokenizer/out_tokenizer.pickle', 'rb') as handle:
            self.out_text_tokenizer = pickle.load(handle)

        self.max_in_len = 0
        with open('./Prediction/models&tokenizer/max_length.json') as json_file:
            data = json.load(json_file)
            self.max_in_len = data["in_max_length"]

        # Variables Code
        self.actual_sequence = []
        self.tracking_move = False
        self.tracking_scroll = False
        self.previous_output = ""
        self.cap = cv2.VideoCapture(camera)
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.model_identify_symb = tf.keras.models.load_model('./Prediction/models&tokenizer/simb_valido.h5')
        self.model_valid_symb = tf.keras.models.load_model('./Prediction/models&tokenizer/comprobar_simb.h5')
        self.model_sequences = tf.keras.models.load_model('./Prediction/models&tokenizer/detector_secuencias.h5')
        self.previous_output = ""
        self.coord_current = 0
        self.coord_previous = 0
        self.depth_activated = False
        self.controller = ActionController()
        self.dictDist = {}

    def include_depth(self, left_cam_num):
        self.stereo_vision = Stereo_Vision()
        self.depth_activated = True

    ######## Auxiliary functions ########
    def output_correction(self, number):
        return (number + 1) % 6

    def input_fingers_dict_generator(self, hands):  # Meter preferible derecha
        hand1 = hands[0]
        puntos = hand1["lmList"]
        bbox = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint = hand1["center"]
        pulgar, info = self.detector.findDistance(puntos[4][:2], puntos[0][:2])
        indice, info = self.detector.findDistance(puntos[8][:2], puntos[0][:2])
        corazon, info = self.detector.findDistance(puntos[12][:2], puntos[0][:2])
        anular, info = self.detector.findDistance(puntos[16][:2], puntos[0][:2])
        menique, info = self.detector.findDistance(puntos[20][:2], puntos[0][:2])
        pulgar_indice, info = self.detector.findDistance(puntos[4][:2], puntos[8][:2])
        magnitud, info = self.detector.findDistance(centerPoint, puntos[0][:2])

        return [[pulgar / magnitud, indice / magnitud, corazon / magnitud, anular / magnitud, menique / magnitud,
                 pulgar_indice / magnitud]], hand1['center'][:2]

    # Function RNN
    def logits_to_sentence(self, logits, tokenizer):
        index_to_words = {idx: word for word, idx in tokenizer.word_index.items()}
        index_to_words[0] = '<empty>'

        return ' '.join([index_to_words[prediction] for prediction in np.argmax(logits, 1)])

    def predict_symbol_valid(self, hands):
        self.dictDist, self.coord_current = self.input_fingers_dict_generator(hands)
        valid_symbol = self.model_valid_symb.predict(np.array(self.dictDist), verbose=0)
        valid_symbol = np.argmax(valid_symbol, axis=1)
        return valid_symbol

    def predict_output(self):
        input_LSTM = " ".join(self.actual_sequence)
        in_text_tokenized_p = self.in_text_tokenizer.texts_to_sequences([input_LSTM])
        in_pad_sentence_p = pad_sequences(in_text_tokenized_p, maxlen=self.max_in_len, padding="post")

        output_LSTM = self.logits_to_sentence(self.model_sequences.predict(in_pad_sentence_p[0:0 + 1])[0],
                                              self.out_text_tokenizer)
        output_LSTM = output_LSTM.split(' <empty>')[0]
        return output_LSTM.split(' ')

    def big_condition(self, list_out):
        first_cond = list_out[0] != "<empty>"
        second_cond = (len(list_out) > len(self.previous_output))
        third_cond = len(self.previous_output) > 0 and list_out[-1] != self.previous_output[-1]
        fourth_cond = len(self.previous_output) > 1 and len(list_out) == len(self.previous_output) and list_out[-2] == self.previous_output[-1] # caso actual 2 2 y previo 3 2 hay un nuevo 2
        return first_cond and (second_cond or third_cond or fourth_cond)

    def do_actions(self, list_out):
        if self.big_condition(list_out):  # output_LSTM != previous_output and: #Si no es el mismo por una nueva accion 0 1 -> 0 1 2, evitar que ejecute dos veces de 0 1 2->2

            if len(list_out) > 2:  # cierres de acciones
                close = list_out[-2]
                if close in ["1", "7"]:
                    print("cierre")  # rehacer cierre
                    self.tracking_move = False
                    self.tracking_scroll = False
            if len(list_out) > 3:  # cierres de acciones
                close = list_out[-3]
                if close in ["1", "7"]:
                    print("cierre")
                    self.tracking_move = False
                    self.tracking_scroll = False

            actual_task = list_out[-1]
            if actual_task in ["1", "7"]:  # son cierres
                actual_task = list_out[-2]  # inicio seguimiento
                if actual_task == "0":
                    self.tracking_move = True
                else:
                    self.tracking_scroll = True
            print(f'{actual_task}actual_task')
            self.controller.take_action(action_number=int(actual_task),
                                        coord=self.coord_current, coord_previous=self.coord_previous)

    ######## Main function ########
    def main_function(self):
        while True:
            success, img = self.cap.read()
            hands, img = self.detector.findHands(img)

            if hands:
                if self.depth_activated:  # Calculate distance if activated
                    hand_depth = self.stereo_vision.calculate_distances(hand_right=hands, frame_right=img,
                                                                        ret_right=success)
                if not self.depth_activated or hand_depth > 15: #If depth not activated continue and if depth over 15 also
                    valid_symbol = self.predict_symbol_valid(hands)

                    if valid_symbol == 1:
                        predicted_symbol = self.model_identify_symb.predict(np.array(self.dictDist), verbose=0)
                        predicted_symbol = self.output_correction(np.argmax(predicted_symbol, axis=1))
                        print(predicted_symbol)
                        time.sleep(0.01)
                        self.actual_sequence.append(str(predicted_symbol[0]))

                        if len(self.actual_sequence) == 10:
                            # coord anteriores menos actuales y pasarselo si es 0  en el caso 6 mirar si es mayor o menor
                            list_out = self.predict_output()
                            print(f'{list_out}input  {" ".join(self.actual_sequence)}')
                            self.do_actions(list_out)
                            self.previous_output = list_out
                            if self.tracking_move:
                                self.controller.take_action(0, self.coord_current, self.coord_previous)
                            elif self.tracking_scroll:
                                self.controller.take_action(6, self.coord_current, self.coord_previous)
                            self.actual_sequence.pop(0)
                self.coord_previous = self.coord_current
            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
