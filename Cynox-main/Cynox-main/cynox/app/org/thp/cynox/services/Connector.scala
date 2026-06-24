package org.thp.cynox.services

import org.thp.cynox.models.HealthStatus
import play.api.libs.json.{JsObject, Json}

trait Connector {
  val name: String
  def status: JsObject           = Json.obj("enabled" -> true)
  def health: HealthStatus.Value = HealthStatus.Ok
}
