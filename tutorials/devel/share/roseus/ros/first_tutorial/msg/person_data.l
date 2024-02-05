;; Auto-generated. Do not edit!


(when (boundp 'first_tutorial::person_data)
  (if (not (find-package "FIRST_TUTORIAL"))
    (make-package "FIRST_TUTORIAL"))
  (shadow 'person_data (find-package "FIRST_TUTORIAL")))
(unless (find-package "FIRST_TUTORIAL::PERSON_DATA")
  (make-package "FIRST_TUTORIAL::PERSON_DATA"))

(in-package "ROS")
;;//! \htmlinclude person_data.msg.html


(defclass first_tutorial::person_data
  :super ros::object
  :slots (_name _age _color ))

(defmethod first_tutorial::person_data
  (:init
   (&key
    ((:name __name) "")
    ((:age __age) 0)
    ((:color __color) "")
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _age (round __age))
   (setq _color (string __color))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:age
   (&optional __age)
   (if __age (setq _age __age)) _age)
  (:color
   (&optional __color)
   (if __color (setq _color __color)) _color)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; uint8 _age
    1
    ;; string _color
    4 (length _color)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; uint8 _age
       (write-byte _age s)
     ;; string _color
       (write-long (length _color) s) (princ _color s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint8 _age
     (setq _age (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; string _color
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _color (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get first_tutorial::person_data :md5sum-) "fcc4ac2f30ce95ce4aadb3be7c765c64")
(setf (get first_tutorial::person_data :datatype-) "first_tutorial/person_data")
(setf (get first_tutorial::person_data :definition-)
      "string name
uint8 age
string color
")



(provide :first_tutorial/person_data "fcc4ac2f30ce95ce4aadb3be7c765c64")


