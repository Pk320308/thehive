package org.thp.cynox.connector.cortex.controllers.v0

import org.thp.scalligraph.query.QueryExecutor
import org.thp.cynox.controllers.v0.CynoxQueryExecutor

import javax.inject.{Inject, Provider}

class CynoxCortexQueryExecutorProvider @Inject() (cynoxQueryExecutor: CynoxQueryExecutor, cortexQueryExecutor: CortexQueryExecutor)
    extends Provider[QueryExecutor] {
  override def get(): QueryExecutor = cynoxQueryExecutor ++ cortexQueryExecutor
}
