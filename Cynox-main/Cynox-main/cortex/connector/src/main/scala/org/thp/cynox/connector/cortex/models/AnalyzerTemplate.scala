package org.thp.cynox.connector.cortex.models

import org.thp.scalligraph.BuildVertexEntity

@BuildVertexEntity
case class AnalyzerTemplate(workerId: String, content: String)
