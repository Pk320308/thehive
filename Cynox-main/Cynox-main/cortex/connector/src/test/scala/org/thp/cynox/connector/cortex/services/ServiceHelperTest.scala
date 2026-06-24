package org.thp.cynox.connector.cortex.services

import org.thp.cortex.client.{CortexClient, TestCortexClientProvider}
import org.thp.scalligraph.models.{Database, Schema}
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.{AppBuilder, EntityName}
import org.thp.cynox.TestAppBuilder
import org.thp.cynox.connector.cortex.models.CynoxCortexSchemaProvider
import org.thp.cynox.models.Organisation
import org.thp.cynox.services._
import play.api.test.PlaySpecification

class ServiceHelperTest extends PlaySpecification with TestAppBuilder {
  override val databaseName: String = "cynoxCortex"
  override def appConfigure: AppBuilder =
    super
      .appConfigure
      .`override`(_.bindToProvider[Schema, CynoxCortexSchemaProvider])
      .`override`(
        _.bindActor[CortexActor]("cortex-actor")
          .bindToProvider[CortexClient, TestCortexClientProvider]
          .bind[Connector, TestConnector]
          .bindToProvider[Schema, CynoxCortexSchemaProvider]
      )

  "service helper" should {
    "filter properly organisations according to supplied config" in testApp { app =>
      val r = app[Database].roTransaction { implicit graph =>
        app[ServiceHelper]
          .organisationFilter(
            app.apply[OrganisationSrv].startTraversal,
            List("*"),
            List("cert")
          )
          .toList
      }
      r must contain(Organisation.administration)

      val r2 = app[Database].roTransaction { implicit graph =>
        app[ServiceHelper]
          .organisationFilter(
            app.apply[OrganisationSrv].startTraversal,
            Nil,
            Nil
          )
          .toList
      }
      r2 must contain(Organisation.administration, Organisation("cert", "cert"))
    }

    "return the correct filtered CortexClient list" in testApp { app =>
      val client = app[CortexClient]
      val r      = app[ServiceHelper].availableCortexClients(Seq(client), EntityName(Organisation.administration.name))

      r must contain(client)
    }
  }
}
