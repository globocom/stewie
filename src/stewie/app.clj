(ns stewie.app
  (use stewie.core
       stewie.db
       noir.core
       somnium.congomongo)
  (:require [noir.server :as server]
            [noir.response :as response]))

(def detect (bucket-detector))

(defpage "/" []
  "Welcome to Stewie!\n")

(defn convert-to-numbers
  "convert hash-map values to numbers"
  [h]
  (into {} (map (fn [[k v]] [k (read-string v)]) h)))

(defpage [:post "/:bucket"] {bucket :bucket :as data}
  (let [data (dissoc data :bucket)
        data (convert-to-numbers data)
        density (detect bucket data)
        data (assoc data :density density)]
    (response/json data)))

(defpage "/test-db" []
  (maybe-init :stewie)
  (let [counter (fetch-and-modify :stewie
                                  {:_id "counter"}
                                  {:$inc {:value 1} }
                                  :return-new true :upsert? true)]
    (str "Welcome to stewie, you're visitor " (or (:value counter) 0))))

(defn -main [& m]
  (let [mode (keyword (or (first m) :dev))
        port (Integer. (get (System/getenv) "PORT" "8080"))]
    (server/start port {:mode mode :ns 'stewie})))
