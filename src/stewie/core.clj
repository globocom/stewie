(ns stewie.core)

; naive implementation
(defn average
  "naive average implementation"
  [coll]
  (/ (reduce + coll) (count coll)))

(defn variance
  "naive variance deviation implementation"
  [coll]
  (let [avg (average coll)]
     (/ (reduce + (map #(Math/pow (- % avg) 2) coll))
      (count coll))))

; naive sliding window
(defn sliding-window-average
  "calculates the average of the first n elements of coll"
  [coll n]
  (average (take n coll)))

(defn sliding-window-variance
  "calculates the variance of the first n elements of coll"
  [coll n]
  (variance (take n coll)))

; O(1) calculator
(defn averager []
  (let [totals (atom {:total 0 :count 0})]
    (fn [n]
      (swap! totals
        (comp
          #(update-in % [:total] + n)
          #(update-in % [:count] inc)
          #(assoc-in % [:average]
            (let [c (get-in % [:count])]
              (if (> c 0)
                (/ (get-in % [:total]) c)))))))))
