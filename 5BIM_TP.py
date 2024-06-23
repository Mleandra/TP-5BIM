#import...
import cv2
from ultralytics import YOLO

class YoloObjectDetection:
    """ Classe pour la détection d'objets
        cette classe contient 2 attributs :
            - model : le modèle d'entrainement pour la détection d'objets
            - colors : les couleurs  appliquées  aux rectangles des objets  détecté
    """

    def __init__(self):
        """
        Initialisation du modèle et des couleurs pour les objets à détecter
        """
        self.model = YOLO('yolov8s.pt')# Le modele choisi est yolov8s
        self.colors = {
            'laptop': (200, 66, 116),  # violet
            'mouse': (255, 0, 255),    # rose
            'default': (0, 255, 0)     # vert
        }

    def detect_and_draw(self, frame):
        """
        Cette fonction permet de détecter les objets sur une image donnée,
          dessine un rectange pour le delimiter et le nom de l'objet

        Il prend en paramètre l'image et retourne l'image avec les delimitations
        """
        resultats = self.model(frame)

        for res in resultats:
            for det in res.boxes:
                #ici on recupere les coordonnées du rectangle
                x1, y1, x2, y2 = map(int, det.xyxy[0])
                conf = det.conf[0]
                classe = int(det.cls[0])#on recupere le numéro de la classe
                label = self.model.names[classe]#on obtient le nom de la classe de l'objet

                # attribution de la couleur en fonction de la classe
                col = self.colors.get(label, self.colors['default'])
                # dessin du rectangle autour de l'objet
                cv2.rectangle(frame, (x1, y1), (x2, y2), col, 3)
                texte_label = f'{label} {conf:.2f}'
                #ajout du background pour les labels
                (w, h), _ = cv2.getTextSize(texte_label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), col, -1)

                #affichage du label
                cv2.putText(frame, texte_label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame

    def detect_objects(self, video):
        """
        cette fonction permet de détecter les objets sur une
        vidéo (en temps réel avec la caméra ou en sur fichier video .mp4 par exemple) 

        elle prend en paramètre le chemin de la video ou l'index de la caméra(0 par défaut)
        """
        cap = cv2.VideoCapture(video)# ouverture de la video ou de la webcam par defaut

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                #Si la frame n'est pas lue correctement,  la boucle s'arrete
                break
            
            #application de la fonction de detection sur la frame
            new_f = self.detect_and_draw(frame)
            #affichage de la nouvelle frame de detection
            cv2.imshow("5BIM-TP : Detection d'objets", new_f)
            # fermeture de la fenêtre en appuyant sur la touche 'q' ou 'Q'
            if cv2.waitKey(1) & 0xFF in (ord('q'), ord('Q')):
                break
        #fermeture de la fenêtre
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":

    video = 0  # 0 pour la caméra 
    #video = '../ma_Video .mp4' si vous voulez utiliser une video sur votre ordinateur
    detecteur = YoloObjectDetection() # creation de l'objet yoloobjectdetection (on instancie la classe)

    detecteur.detect_objects(video) # lancement de la detection