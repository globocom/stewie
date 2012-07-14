(ns stewie.app
  (use stewie.core
       stewie.crypto
       stewie.db
       noir.core
       somnium.congomongo)
  (:require [noir.server :as server]
            [noir.response :as response]))

(def detect (bucket-detector))
(def collection :buckets)

(defpage "/" []
  "Welcome to Stewie!\n")

(defn convert-to-numbers
  "convert hash-map values to numbers"
  [h]
  (into {} (map (fn [[k v]] [k (read-string v)]) h)))

(defpage "/:bucket" {bucket :bucket}
  (let [taken (has-data collection bucket)
        new-token (token bucket)]
    (if taken
      (assoc
        (response/json {:error "token already taken"})
        :status 410)
      (response/json {:token new-token}))))

(defpage [:post "/:bucket"] {bucket :bucket :as data}
  (if (= (str (data :token)) (token bucket))
    (let [data (dissoc data :bucket :token)
          data (convert-to-numbers data)
          density (detect bucket data)
          result {:data data :density density}
          id (save-data collection bucket result)]
      (response/json result))
    (assoc
      (response/json {:error "invalid token"})
      :status 403)))

(defn -main [& m]
  (let [mode (keyword (or (first m) :dev))
        port (Integer. (get (System/getenv) "PORT" "8080"))]
    (maybe-init collection)
    (server/start port {:mode mode :ns 'stewie})))
