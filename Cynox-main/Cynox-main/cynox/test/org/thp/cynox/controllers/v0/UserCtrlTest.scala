package org.thp.cynox.controllers.v0

import akka.stream.Materializer
import org.thp.scalligraph.models.Database
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.{AuthenticationError, EntityName}
import org.thp.cynox.TestAppBuilder
import org.thp.cynox.dto.v0.OutputUser
import org.thp.cynox.services.UserSrv
import play.api.libs.json.Json
import play.api.test.{FakeRequest, PlaySpecification}

case class TestUser(login: String, name: String, roles: Set[String], organisation: String, hasKey: Boolean, status: String)

object TestUser {

  def apply(user: OutputUser): TestUser =
    TestUser(user.login, user.name, user.roles, user.organisation, user.hasKey, user.status)
}

class UserCtrlTest extends PlaySpecification with TestAppBuilder {
  "user controller" should {
    "search users" in testApp { app =>
      val request = FakeRequest("POST", "/api/v0/user/_search?range=all&sort=%2Bname")
        .withJsonBody(
          Json.parse(
            """{"query": {"_and": [{"status": "Ok"}, {"_not": {"_is": {"login": "socadmin@cynox.local"}}}, {"_not": {"_is": {"login": "socuser@cynox.local"}}}]}}"""
          )
        )
        .withHeaders("user" -> "socadmin@cynox.local")

      val result = app[UserCtrl].search(request)
      status(result) must_=== 200

      val resultUsers = contentAsJson(result)(defaultAwaitTimeout, app[Materializer])
      val expected =
        Seq(
          TestUser(
            login = "socro@cynox.local",
            name = "socro",
            roles = Set("read"),
            organisation = "soc",
            hasKey = false,
            status = "Ok"
          )
        )

      resultUsers.as[Seq[OutputUser]].map(TestUser.apply) shouldEqual expected
    }

    "create a new user" in testApp { app =>
      val request = FakeRequest("POST", "/api/v0/user")
        .withJsonBody(Json.parse("""{"login": "certXX@cynox.local", "name": "new user", "roles": ["read", "write", "alert"]}"""))
        .withHeaders("user" -> "certadmin@cynox.local")

      val result = app[UserCtrl].create(request)
      status(result) must_=== 201

      val resultUser = contentAsJson(result).as[OutputUser]
      val expected = TestUser(
        login = "certxx@cynox.local",
        name = "new user",
        roles = Set("read", "write", "alert"),
        organisation = "cert",
        hasKey = false,
        status = "Ok"
      )

      TestUser(resultUser) must_=== expected
    }

    "update a user" in testApp { app =>
      val request = FakeRequest("POST", "/api/v0/user/certuser@cynox.local")
        .withJsonBody(Json.parse("""{"name": "new name"}"""))
        .withHeaders("user" -> "certadmin@cynox.local")

      val result = app[UserCtrl].update("certuser@cynox.local")(request)
      status(result) must beEqualTo(200).updateMessage(s => s"$s\n${contentAsString(result)}")

      val resultUser = contentAsJson(result).as[OutputUser]
      resultUser.name must_=== "new name"
    }

    "lock an user" in testApp { app =>
      val authRequest1 = FakeRequest("POST", "/api/v0/login")
        .withJsonBody(Json.parse("""{"user": "certuser@cynox.local", "password": "my-secret-password"}"""))
      val authResult1 = app[AuthenticationCtrl].login(authRequest1)
      status(authResult1) must_=== 200

      val request = FakeRequest("POST", "/api/v0/user/certuser@cynox.local")
        .withJsonBody(Json.parse("""{"status": "Locked"}"""))
        .withHeaders("user" -> "certadmin@cynox.local")

      val result = app[UserCtrl].update("certuser@cynox.local")(request)
      status(result) must_=== 200
      val resultUser = contentAsJson(result).as[OutputUser]
      resultUser.status must_=== "Locked"

      // then authentication must fail
      val authRequest2 = FakeRequest("POST", "/api/v0/login")
        .withJsonBody(Json.parse("""{"user": "certuser@cynox.local", "password": "my-secret-password"}"""))
      val authResult2 = app[AuthenticationCtrl].login(authRequest2)
      status(authResult2) must_=== 401
    }

    "unlock an user" in testApp { app =>
      val keyAuthRequest = FakeRequest("GET", "/api/v0/user/current")
        .withHeaders("Authorization" -> "Bearer azertyazerty")

      status(app[UserCtrl].current(keyAuthRequest)) must throwA[AuthenticationError]

      val request = FakeRequest("POST", "/api/v0/user/certro@cynox.local")
        .withJsonBody(Json.parse("""{"status": "Ok"}"""))
        .withHeaders("user" -> "certadmin@cynox.local")

      val result = app[UserCtrl].update("certro@cynox.local")(request)
      status(result) must beEqualTo(200).updateMessage(s => s"$s\n${contentAsString(result)}")
      val resultUser = contentAsJson(result).as[OutputUser]
      resultUser.status must_=== "Ok"

      status(app[UserCtrl].current(keyAuthRequest)) must_=== 200
    }

    "remove a user (lock)" in testApp { app =>
      val request = FakeRequest("DELETE", "/api/v0/user/certro@cynox.local")
        .withHeaders("user" -> "certadmin@cynox.local")
      val result = app[UserCtrl].lock("certro@cynox.local")(request)

      status(result) must beEqualTo(204)

      val requestGet = FakeRequest("POST", "/api/v0/user/certro@cynox.local")
        .withHeaders("user" -> "certadmin@cynox.local")
      val resultGet = app[UserCtrl].get("certro@cynox.local")(requestGet)

      status(resultGet) must_=== 200
      contentAsJson(resultGet).as[OutputUser].status must beEqualTo("Locked")
    }

    "remove a user (force)" in testApp { app =>
      val request = FakeRequest("DELETE", "/api/v0/user/certro@cynox.local/force")
        .withHeaders("user" -> "certadmin@cynox.local")
      val result = app[UserCtrl].delete("certro@cynox.local")(request)

      status(result) must beEqualTo(204)

      app[Database].roTransaction { implicit graph =>
        app[UserSrv].get(EntityName("certro@cynox.local")).exists
      } must beFalse
    }
  }
}
