package org.thp.cynox.services

import org.thp.scalligraph.EntityName
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models.{Database, DummyUserSrv}
import org.thp.cynox.TestAppBuilder
import org.thp.cynox.models._
import play.api.test.PlaySpecification

class OrganisationSrvTest extends PlaySpecification with TestAppBuilder {
  implicit val authContext: AuthContext = DummyUserSrv(userId = "admin@cynox.local").authContext

  "organisation service" should {
    "create an organisation" in testApp { app =>
      app[Database].tryTransaction { implicit graph =>
        app[OrganisationSrv].create(Organisation(name = "orga1", "no description"))
      } must beSuccessfulTry
    }

    "get an organisation by its name" in testApp { app =>
      app[Database].tryTransaction { implicit graph =>
        app[OrganisationSrv].getOrFail(EntityName("cert"))
      } must beSuccessfulTry
    }
  }
}
