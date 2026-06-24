package org.thp.cynox.connector.cortex.controllers.v0

import org.thp.cynox.TestAppBuilder
import org.thp.cynox.connector.cortex.dto.v0.OutputWorker
import play.api.test.{FakeRequest, PlaySpecification}

class AnalyzerCtrlTest extends PlaySpecification with TestAppBuilder {

  "analyzer controller" should {
    "list analyzers" in testApp { app =>
      val request = FakeRequest("GET", s"/api/connector/cortex/analyzer?range=all").withHeaders("user" -> "certuser@cynox.local")
      val result  = app[AnalyzerCtrl].list(request)

      status(result) shouldEqual 200

      val resultList = contentAsJson(result).as[Seq[OutputWorker]]

      resultList must beEmpty
    }
  }
}
