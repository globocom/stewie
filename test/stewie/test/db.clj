(ns stewie.test.db
  (:use stewie.db
  	    somnium.congomongo
  	    midje.sweet))

(fact "mongo connection works"
	(let [db (maybe-init :test)]
		(collection-exists? :test) => true))
