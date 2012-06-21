(ns stewie.test.core
  (:use [stewie.core])
  (:use midje.sweet))

(fact "average reference implementation is correct"
  (average (repeat 10 1)) => 1
  (average (range 11)) => 5)

(fact "variance reference implementation is correct"
  (variance (repeat 10 1)) => 0.0
  (variance (range 11)) => 10.0
  (variance [1 2 3 4 5]) => 2.0
  (variance [1 2 3 4]) => 1.25)

(fact "sliding window average reference implementation is correct"
  (sliding-window-average (repeat 10 1) 5) => 1
  (sliding-window-average (range 11) 5) => 2)

(fact "sliding window variance reference implementation is correct"
  (sliding-window-variance (repeat 20 1) 10) => 0.0
  (sliding-window-variance (range 1 20) 5) => 2.0
  (sliding-window-variance (range 1 20) 4) => 1.25)

(fact "accumulator evaluates average and variance"
  (let [acc (accumulator)
        input (range 11)
        result (last (for [x input] (acc x)))]
    (result :average) => (average input)
    (result :variance) => (variance input)))

(fact "density implementation is correct"
  (density 0 0 1) => (/ 1 (Math/sqrt (* 2 Math/PI)))
  (density 1 0 1) => (* (Math/exp -1/2) (density 0 0 1))
  (density 2 0 1) => (* (Math/exp -2) (density 0 0 1))
  (density -1 0 1) => (density 1 0 1)
  (density 6 5 1) => (density 1 0 1))

(fact "single-variable-detector returns value propability"
  (let [det (single-variable-detector)
        input (range 11)
        result (last (for [x input] (det x)))]
    result => (density (last input) (average input) (variance input))))

(fact "detector returns propability of one variable"
  (let [det (detector)
        input (range 11)
        result (last (for [x input] (det {:x x})))]
    result => (density (last input) (average input) (variance input))))

(fact "detector returns propability of two variables"
  (let [det (detector)
        input (range 11)
        result (last (for [x input] (det {:x x :y x})))]
    result => (Math/pow (density 10 5 10) 2)))
