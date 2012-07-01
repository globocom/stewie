(ns stewie.app
  (:use noir.core)
  (:require [noir.server :as server]))

(defpage "/" []
    "Welcome to Stewie!")

(defn -main [& m]
  (let [mode (keyword (or (first m) :dev))
        port (Integer. (get (System/getenv) "PORT" "8080"))]
    (server/start port {:mode mode
                        :ns 'my-noir})))
