package org.thp.cynox

import akka.actor.Actor

class DummyActor extends Actor {
  override def receive: Receive = PartialFunction.empty
}
