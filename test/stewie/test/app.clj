(ns stewie.test.app
  (:use stewie.app
        stewie.core
        stewie.crypto
        stewie.db
        stewie.test.db
        midje.sweet)
  (:require [cheshire.core :as json]
            [noir.util.test :as noir]
            [somnium.congomongo :as mongo]))

(fact "homepage returns status 200"
  (-> (noir/send-request "/") :status) => 200)

(fact "post to bucket returns json"
  (let [token (token "bucket")
        response (noir/send-request
          [:post "/bucket"]
          {"x" "1" "token" token})]
    (response :status) => 200
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "density") => "NaN"))

(fact "post to bucket has memory"
  (noir/with-noir
    (let [token (token "memory")
          input (range 11)
          post-to-bucket (fn [x] (noir/send-request
            [:post "/memory"]
            {"x" (str x) "token" token}))
          response (last (for [x input] (post-to-bucket x)))
          json-response (json/parse-string (response :body))]
      (json-response "density") => (density (last input) (average input) (variance input)))))

(fact "post to bucket persists data in db"
  (let [token (token "temp")
        cleaned (clean-bucket! collection :temp)
        response (noir/send-request [:post "/temp"] {"x" "1" "token" token})
        fetch-count (mongo/fetch-count collection :where {:bucket :temp})]
    fetch-count => 1))

(fact "post to bucket requires token"
  (let [cleaned (clean-bucket! collection :temp)
        response (noir/send-request [:post "/temp"] {"x" "1"})]
    (response :status) => 403
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "error") => "invalid token"))

(fact "post to bucket validates token"
  (let [cleaned (clean-bucket! collection :temp)
        response (noir/send-request [:post "/temp"] {"x" "1" "token" "wrong-token"})
        fetch-count (mongo/fetch-count collection :where {:bucket :temp})]
    (response :status) => 403
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "error") => "invalid token"
    fetch-count => 0))

(fact "get to bucket returns token"
  (let [initiated (maybe-init collection)
        cleaned (clean-bucket! collection :token)
        response (noir/send-request "/token")]
    (response :status) => 200
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "token") => (token "token")))

(fact "get to bucket does not return token if it is already taken"
  (let [token (token "token")
        initiated (maybe-init collection)
        cleaned (clean-bucket! collection :token)
        response (noir/send-request [:post "/token"] {"x" "1" "token" token})
        response (noir/send-request "/token")]
    (response :status) => 410
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "error") => "token already taken"))
