(define (domain tps)
    (:requirements :strips)
    (:predicates (connected ?x ?y)  (delivered ?x)  (in ?x))
    (:action deliver
        :parameters (?x)
        :precondition (and (in ?x) (not (delivered ?x)))
        :effect (delivered ?x)
    )
     (:action go_to
        :parameters (?x ?y)
        :precondition (and (connected ?x ?y) (in ?x))
        :effect (and (not (in ?x)) (in ?y))
    )
)