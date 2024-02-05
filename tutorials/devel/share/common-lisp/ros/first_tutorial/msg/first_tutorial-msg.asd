
(cl:in-package :asdf)

(defsystem "first_tutorial-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "person_data" :depends-on ("_package_person_data"))
    (:file "_package_person_data" :depends-on ("_package"))
  ))