(define (problem puzzle_problem)
    (:domain puzzle)
    
    (:objects c0 c1 c2 c3 c4 c5 c6 c7 c8 p0 p1 p2 p3 p4 p5 p6 p7 p8)
    (:init (PIECE c0) (PIECE c1) (PIECE c2) (PIECE c3) (PIECE c4) (PIECE c5) (PIECE c6) (PIECE c7) (PIECE c8) (POSITION p0) (POSITION p1) (POSITION p2) (POSITION p3) (POSITION p4) (POSITION p5) (POSITION p6) (POSITION p7) (POSITION p8) (at p0 c0) (at p1 c1) (at p2 c2) (at p3 c3) (at p4 c4) (at p5 c5) (at p6 c6) (at p7 c8) (at p8 c7))
    (:goal (and (at p0 c0) (at p1 c1) (at p2 c2) (at p3 c3) (at p4 c4) (at p5 c5) (at p6 c6) (at p7 c7) (at p8 c8)))
)