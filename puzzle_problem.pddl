(define (problem puzzle_problem)
    (:domain puzzle2)
    
    (:objects c1 c10 c11 c12 c2 c3 c4 c5 c6 c7 c8 c9 p1 p10 p11 p12 p2 p3 p4 p5 p6 p7 p8 p9)
    (:init (PIECE c1) (PIECE c10) (PIECE c11) (PIECE c12) (PIECE c2) (PIECE c3) (PIECE c4) (PIECE c5) (PIECE c6) (PIECE c7) (PIECE c8) (PIECE c9) (POSITION p1) (POSITION p10) (POSITION p11) (POSITION p12) (POSITION p2) (POSITION p3) (POSITION p4) (POSITION p5) (POSITION p6) (POSITION p7) (POSITION p8) (POSITION p9) (at p1 c2) (at p10 c10) (at p11 c12) (at p12 c11) (at p2 c4) (at p3 c8) (at p4 c5) (at p5 c1) (at p6 c3) (at p7 c9) (at p8 c6) (at p9 c7))
    (:goal (and (at p1 c1) (at p2 c2) (at p3 c3) (at p4 c4) (at p5 c5) (at p6 c6) (at p7 c7) (at p8 c8) (at p9 c9) (at p10 c10) (at p11 c11) (at p12 c12)))
)