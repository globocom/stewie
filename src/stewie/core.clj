(ns stewie.core)

(defn accumulator []
  "Generages an accumulator that will return average and variance in O(1)

  It keeps an internal state of:
  {
    :total sum(x_i),
    :sq_total sum(x_i ^ 2),
    :count count(x_i),
  }

  Result is:
  {
    :average      :total / :count
    :variance     :sq_total / :count - :average ^ 2
  }

  "
  (let [totals (atom {:total 0, :count 0, :sq_total 0})]
    (fn [n]
      (let [update_totals (comp #(update-in % [:count] inc)
                                #(update-in % [:total] + n)
                                #(update-in % [:sq_total] + (Math/pow n 2)))
            result (swap! totals update_totals)
            cnt (result :count)
            avg (/ (result :total) cnt)]
        {:average avg
         :variance (- (/ (result :sq_total) cnt) (Math/pow avg 2))}))))

; See http://en.wikipedia.org/wiki/Probability_density_function
(defn density [x average variance]
  "Calculates probability density function"
  (let [sigma (Math/sqrt variance)
        divisor (* sigma (Math/sqrt (* 2 Math/PI)))
        exponent (/ (Math/pow (- x average) 2) (* 2 variance))]
    (/ (Math/exp (- 0 exponent)) divisor)))

(defn detector []
  "Given an stream input of points, returns the probability density for the last input point"
  (let [acc (accumulator)]
    (fn [x]
      (let [state (acc x)]
        (density x (state :average) (state :variance))))))

; Reference implementations
(defn average
  "naive average implementation"
  [coll]
  (/ (reduce + coll) (count coll)))

(defn variance
  "naive variance implementation"
  [coll]
  (let [avg (average coll)]
     (/ (reduce + (map #(Math/pow (- % avg) 2) coll))
      (count coll))))

(defn sliding-window-average
  "calculates the average of the first n elements of coll"
  [coll n]
  (average (take n coll)))

(defn sliding-window-variance
  "calculates the variance of the first n elements of coll"
  [coll n]
  (variance (take n coll)))
