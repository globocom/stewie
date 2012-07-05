(defproject stewie "1.0.0-SNAPSHOT"
  :description "FIXME: write description"
  :dependencies [[org.clojure/clojure "1.3.0"]
                 [noir "1.2.1"]]
  :dev-dependencies [[midje "1.4.0"]
                     [lein-midje "1.0.9"]
                     [lein-noir "1.2.1"]
                     [com.stuartsierra/lazytest "1.2.3"]]
  :repositories {"stuart" "http://stuartsierra.com/maven2"}
  :main stewie.app)
