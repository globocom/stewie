(ns stewie.test.app
  (:use [stewie.app])
  (:use [midje.sweet])
  (:require [noir.util.test :as noir]))

(fact "homepage returns status 200"
	(-> (noir/send-request "/") :status) => 200)
