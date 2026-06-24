package org.thp.cynox.services.notification.triggers

import org.thp.scalligraph.EntityName
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models.{Database, DummyUserSrv}
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.cynox.TestAppBuilder
import org.thp.cynox.services.UserOps._
import org.thp.cynox.services._
import play.api.test.PlaySpecification

class TaskAssignedTest extends PlaySpecification with TestAppBuilder {
  implicit val authContext: AuthContext = DummyUserSrv(userId = "certadmin@cynox.local").authContext

  "task assigned trigger" should {
    "be properly triggered on task assignment" in testApp { app =>
      app[Database].tryTransaction { implicit graph =>
        for {
          task1 <- app[TaskSrv].startTraversal.has(_.title, "case 1 task 1").getOrFail("Task")
          user1 <- app[UserSrv].startTraversal.getByName("certuser@cynox.local").getOrFail("User")
          user2 <- app[UserSrv].startTraversal.getByName("certadmin@cynox.local").getOrFail("User")
          _     <- app[TaskSrv].assign(task1, user1)
          _     <- app[AuditSrv].flushPendingAudit()
          audit <- app[AuditSrv].startTraversal.has(_.objectId, task1._id.toString).getOrFail("Audit")
          orga  <- app[OrganisationSrv].get(EntityName("cert")).getOrFail("Organisation")
          taskAssignedTrigger = new TaskAssigned(app[TaskSrv])
          _                   = taskAssignedTrigger.filter(audit, Some(task1), orga, Some(user1)) must beTrue
          _                   = taskAssignedTrigger.filter(audit, Some(task1), orga, Some(user2)) must beFalse
        } yield ()
      } must beASuccessfulTry
    }
  }
}
