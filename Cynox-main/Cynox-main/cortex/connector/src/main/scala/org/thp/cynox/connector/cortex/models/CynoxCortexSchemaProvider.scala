package org.thp.cynox.connector.cortex.models

import org.thp.scalligraph.models.Schema
import org.thp.cynox.models.CynoxSchemaDefinition

import javax.inject.{Inject, Provider, Singleton}

@Singleton
class CynoxCortexSchemaProvider @Inject() (cynoxSchema: CynoxSchemaDefinition, cortexSchema: CortexSchemaDefinition) extends Provider[Schema] {
  override lazy val get: Schema = cynoxSchema + cortexSchema
}
