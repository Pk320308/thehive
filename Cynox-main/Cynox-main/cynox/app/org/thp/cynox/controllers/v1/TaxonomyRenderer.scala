package org.thp.cynox.controllers.v1

import org.thp.scalligraph.traversal.{Converter, Traversal}
import org.thp.cynox.models.Taxonomy
import org.thp.cynox.services.TaxonomyOps._
import play.api.libs.json._

trait TaxonomyRenderer extends BaseRenderer[Taxonomy] {

  def enabledStats: Traversal.V[Taxonomy] => Traversal[JsValue, Boolean, Converter[JsValue, Boolean]] =
    _.enabled.domainMap(l => JsBoolean(l))

  def taxoStatsRenderer(extraData: Set[String]): Traversal.V[Taxonomy] => JsTraversal = { implicit traversal =>
    baseRenderer(
      extraData,
      traversal,
      {
        case (f, "enabled") => addData("enabled", f)(enabledStats)
        case (f, _)         => f
      }
    )
  }
}
