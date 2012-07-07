(ns stewie.test.crypto
  (:use stewie.crypto
        midje.sweet))

(fact "always generate the same token for same key"
	(token "key") => (token "key"))

(fact "creates different tokens for different keys"
	(= (token "key") (token "key2")) => false)

(fact "keys have always the same size"
	(count (token "key")) => 40
	(count (token "a_really_big_key_with_several_characters")) => 40)

(fact "keys are an hexadecimal value"
	(every? identity  (map #(contains? (set "0123456789abcdef") %)
		(token "key"))) => true)
