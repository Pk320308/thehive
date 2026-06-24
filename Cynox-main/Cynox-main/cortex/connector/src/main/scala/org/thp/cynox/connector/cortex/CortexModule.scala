package org.thp.cynox.connector.cortex

import com.google.inject.AbstractModule
import net.codingwell.scalaguice.{ScalaModule, ScalaMultibinder}
import org.thp.scalligraph.models.UpdatableSchema
import org.thp.scalligraph.query.QueryExecutor
import org.thp.cynox.connector.cortex.controllers.v0.{CortexQueryExecutor => CortexQueryExecutorV0}
import org.thp.cynox.connector.cortex.models.CortexSchemaDefinition
import org.thp.cynox.connector.cortex.services.notification.notifiers.{RunAnalyzerProvider, RunResponderProvider}
import org.thp.cynox.connector.cortex.services.{Connector, CortexActor}
import org.thp.cynox.services.notification.notifiers.NotifierProvider
import org.thp.cynox.services.{Connector => CynoxConnector}
import play.api.libs.concurrent.AkkaGuiceSupport
import play.api.routing.{Router => PlayRouter}
import play.api.{Configuration, Environment, Logger}

class CortexModule(environment: Environment, configuration: Configuration) extends AbstractModule with ScalaModule with AkkaGuiceSupport {
  lazy val logger: Logger = Logger(getClass)

  override def configure(): Unit = {
    val routerBindings = ScalaMultibinder.newSetBinder[PlayRouter](binder)
    routerBindings.addBinding.toProvider[CortexRouter]
    val queryExecutorBindings = ScalaMultibinder.newSetBinder[QueryExecutor](binder)
    queryExecutorBindings.addBinding.to[CortexQueryExecutorV0]
    val connectorBindings = ScalaMultibinder.newSetBinder[CynoxConnector](binder)
    connectorBindings.addBinding.to[Connector]
    val schemaBindings = ScalaMultibinder.newSetBinder[UpdatableSchema](binder)
    schemaBindings.addBinding.to[CortexSchemaDefinition]

    val notifierBindings = ScalaMultibinder.newSetBinder[NotifierProvider](binder)
    notifierBindings.addBinding.to[RunResponderProvider]
    notifierBindings.addBinding.to[RunAnalyzerProvider]

    bindActor[CortexActor]("cortex-actor")
    ()
  }
}
