package org.thp.cynox.services

import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models._
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.cynox.TestAppBuilder
import org.thp.cynox.models._
import org.thp.cynox.services.DataOps._
import play.api.test.PlaySpecification

class DataSrvTest extends PlaySpecification with TestAppBuilder {
  implicit val authContext: AuthContext = DummyUserSrv(userId = "certuser@cynox.local", organisation = "cert").authContext

  "data service" should {
    "create not existing data" in testApp { app =>
      val existingData = app[Database].roTransaction(implicit graph => app[DataSrv].startTraversal.getByData("h.fr").getOrFail("Data")).get
      val newData      = app[Database].tryTransaction(implicit graph => app[DataSrv].create(existingData))
      newData must beSuccessfulTry.which(data => data._id shouldEqual existingData._id)
    }

    "get related observables" in testApp { app =>
      app[Database].tryTransaction { implicit graph =>
        app[ObservableSrv].create(
          Observable(
            message = Some("love"),
            tlp = 1,
            ioc = false,
            sighted = true,
            ignoreSimilarity = None,
            dataType = "domain",
            tags = Seq("tagX")
          ),
          "love.com"
        )
      }

      app[Database].roTransaction(implicit graph => app[DataSrv].startTraversal.getByData("love.com").observables.exists must beTrue)
    }
  }
}
