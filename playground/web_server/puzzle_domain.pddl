(define (domain puzzle)
    (:requirements :strips)
    (:predicates (PIECE ?x)  (POSITION ?p)  (at ?p ?x))
    (:action swap
        :parameters (?px ?x ?py ?y)
        :precondition (and (POSITION ?px) (POSITION ?py) (PIECE ?x) (PIECE ?y) (at ?px ?x) (at ?py ?y))
        :effect (and (at ?px ?y) (at ?py ?x) (not (at ?px ?x)) (not (at ?py ?y)))
    )
)