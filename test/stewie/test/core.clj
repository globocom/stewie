(ns stewie.test.core
  (:use [stewie.core])
  (:use midje.sweet))


(fact "average works"
  (average (repeat 10 1)) => 1
  (average (range 11)) => 5)

(fact "variance works"
  (variance (repeat 10 1)) => 0.0
  (variance [1 2 3 4 5]) => 2.0
  (variance [1 2 3 4]) => 1.25)

(fact "sliding window average works"
  (sliding-window-average (repeat 10 1) 5) => 1
  (sliding-window-average (range 11) 5) => 2)

(fact "sliding window variance works"
  (sliding-window-variance (repeat 20 1) 10) => 0.0
  (sliding-window-variance (range 1 20) 5) => 2.0
  (sliding-window-variance (range 1 20) 4) => 1.25)

(fact "averager can count and sum"
  (let [summer (averager)
        result (last (repeatedly 10 #(summer 10)))]
    (result :total) => 100
    (result :count) => 10
    (result :average) => 10))
