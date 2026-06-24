package org.thp.cynox.connector.cortex.services

import org.thp.cortex.client.{CortexClient, TestCortexClientProvider}
import org.thp.scalligraph.AppBuilder
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models._
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.cynox.TestAppBuilder
import org.thp.cynox.connector.cortex.models.CynoxCortexSchemaProvider
import org.thp.cynox.models.Permissions
import org.thp.cynox.services._
import play.api.libs.json.Json
import play.api.test.PlaySpecification

class ResponderSrvTest extends PlaySpecification with TestAppBuilder {
  implicit val authContext: AuthContext =
    DummyUserSrv(userId = "certuser@cynox.local", organisation = "cert", permissions = Permissions.all).authContext

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

  "responder service" should {
    "fetch responders by type" in testApp { app =>
      val task = app[Database].roTransaction { implicit graph =>
        app[TaskSrv].startTraversal.has(_.title, "case 1 task 1").head
      }

      val r = await(app[ResponderSrv].getRespondersByType("case_task", task._id))

      r.find(_._1.name == "respTest1") must beSome
    }

    "search responders" in testApp { app =>
      val r = await(app[ResponderSrv].searchResponders(Json.obj("query" -> Json.obj())))

      r.size must be greaterThan 0
      r.head._2 shouldEqual Seq("test")
    }
  }
}
