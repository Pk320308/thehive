import Dependencies._
import com.typesafe.sbt.packager.Keys.bashScriptDefines
import org.thp.ghcl.Milestone

val cynoxVersion         = "4.1.24-1"
val scala212               = "2.12.13"
val scala213               = "2.13.1"
val supportedScalaVersions = List(scala212, scala213)

organization in ThisBuild := "org.thp"
scalaVersion in ThisBuild := scala212
crossScalaVersions in ThisBuild := supportedScalaVersions
resolvers in ThisBuild ++= Seq(
  Resolver.mavenLocal,
  "Oracle Released Java Packages" at "https://download.oracle.com/maven",
  "Cynox project repository" at "https://dl.bintray.com/cynox-project/maven/"
)
scalacOptions in ThisBuild ++= Seq(
  "-encoding",
  "UTF-8",
  "-deprecation",         // Emit warning and location for usages of deprecated APIs.
  "-feature",             // Emit warning and location for usages of features that should be imported explicitly.
  "-unchecked",           // Enable additional warnings where generated code depends on assumptions.
  "-Xlint",               // Enable recommended additional warnings.
  "-Ywarn-numeric-widen", // Warn when numerics are widened.
  "-Ywarn-value-discard", // Warn when non-Unit expression results are unused
  //"-Xfatal-warnings",   // Fail the compilation if there are any warnings.
  //"-Ywarn-adapted-args",// Warn if an argument list is modified to match the receiver.
  //"-Ywarn-dead-code",   // Warn when dead code is identified.
  //"-Ywarn-inaccessible",// Warn about inaccessible types in method signatures.
  //"-Ywarn-nullary-override",// Warn when non-nullary overrides nullary, e.g. def foo() over def foo.
  //"-Ylog-classpath",
  //"-Xlog-implicits",
  //"-Yshow-trees-compact",
  //"-Yshow-trees-stringified",
  //"-Ymacro-debug-lite",
  "-Xlog-free-types",
  "-Xlog-free-terms",
  "-Xprint-types"
)
fork in Test in ThisBuild := true
javaOptions in Test in ThisBuild += s"-Dlogger.file=${file("test/resources/logback-test.xml").getAbsoluteFile}"
javaOptions in ThisBuild ++= Seq(
  "-Xms512M",
  "-Xmx2048M",
  "-Xss1M",
  "-XX:+CMSClassUnloadingEnabled",
  "-XX:MaxPermSize=256M",
  "-XX:MaxMetaspaceSize=512m"
)
scalafmtConfig in ThisBuild := file(".scalafmt.conf")
scalacOptions in ThisBuild ++= {
  CrossVersion.partialVersion((Compile / scalaVersion).value) match {
    case Some((2, n)) if n >= 13 => "-Ymacro-annotations" :: Nil
    case _                       => Nil
  }
}
libraryDependencies in ThisBuild ++= {
  CrossVersion.partialVersion(scalaVersion.value) match {
    case Some((2, n)) if n >= 13 => Nil
    case _                       => compilerPlugin(macroParadise) :: Nil
  }
}
dependencyOverrides in ThisBuild ++= Seq(
  akkaActor,
  logbackClassic
)
val securityUpdates = Seq(
  "com.fasterxml.jackson.module" %% "jackson-module-scala" % "2.12.6",
  "com.fasterxml.jackson.core"    % "jackson-databind"     % "2.12.6.1",
  "org.yaml"                      % "snakeyaml"            % "1.30"
)
dependencyOverrides in ThisBuild ++= securityUpdates
PlayKeys.includeDocumentationInBinary := false
milestoneFilter := ((milestone: Milestone) => milestone.title.startsWith("4"))

lazy val scalligraph = (project in file("ScalliGraph"))
  .settings(name := "scalligraph")

lazy val cynox = (project in file("."))
  .enablePlugins(PlayScala)
  .dependsOn(cynoxCore, cynoxCortex, cynoxMisp, cynoxFrontend, cynoxMigration)
  .settings(
    name := "cynox",
    version := cynoxVersion,
    crossScalaVersions := Nil,
    PlayKeys.playMonitoredFiles ~= (_.filter(f => f.compareTo(file("frontend/app").getAbsoluteFile) != 0)),
    PlayKeys.devSettings += "play.server.provider" -> "org.thp.cynox.CustomAkkaHttpServerProvider",
//    Universal / mappings ++= (cynoxMigration / Universal / mappings).value,
    Compile / run := {
      (cynoxFrontend / gruntDev).value
      (Compile / run).evaluated
    },
    discoveredMainClasses in Compile := Seq("play.core.server.ProdServerStart", "org.thp.cynox.migration.Migrate", "org.thp.cynox.cloner.Cloner"),
    mainClass in (Compile, bashScriptDefines) := None,
    makeBashScripts ~= {
      _.map {
        case (f, "bin/prod-server-start") => (f, "bin/cynox")
        case other                        => other
      }
    },
    clean := {
      (clean in scalligraph).value
      (clean in cynoxCore).value
      (clean in cynoxDto).value
      (clean in cynoxClient).value
      (clean in cynoxFrontend).value
      (clean in cynoxCortex).value
      (clean in cynoxMisp).value
      (clean in cortexClient).value
      (clean in mispClient).value
      (clean in cynoxMigration).value
      (clean in clientCommon).value
      (clean in cortexDto).value
    },
    test := {
      (test in Test in scalligraph).value
      (test in Test in cynoxCore).value
      (test in Test in cynoxDto).value
      (test in Test in cynoxClient).value
      (test in Test in cynoxFrontend).value
      (test in Test in cynoxCortex).value
      (test in Test in cynoxMisp).value
      (test in Test in cortexClient).value
      (test in Test in mispClient).value
      (test in Test in cynoxMigration).value
      (test in Test in clientCommon).value
      (test in Test in cortexDto).value
    },
    testQuick := {
      (testQuick in Test in scalligraph).evaluated
      (testQuick in Test in cynoxCore).evaluated
      (testQuick in Test in cynoxDto).evaluated
      (testQuick in Test in cynoxClient).evaluated
      (testQuick in Test in cynoxFrontend).evaluated
      (testQuick in Test in cynoxCortex).evaluated
      (testQuick in Test in cynoxMisp).evaluated
      (testQuick in Test in cortexClient).evaluated
      (testQuick in Test in mispClient).evaluated
      (testQuick in Test in cynoxMigration).evaluated
      (testQuick in Test in clientCommon).evaluated
      (testQuick in Test in cortexDto).evaluated
    }
  )

lazy val cynoxCore = (project in file("cynox"))
  .enablePlugins(PlayScala)
  .dependsOn(scalligraph)
  .dependsOn(scalligraph % "test -> test")
  .dependsOn(cortexClient % "test -> test")
  .dependsOn(cynoxDto)
  .dependsOn(clientCommon)
  .dependsOn(cynoxClient % Test)
  .settings(
    name := "cynox-core",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      chimney,
      guice,
      akkaCluster,
      akkaClusterTyped,
      akkaClusterTools,
      zip4j,
      ws,
      specs % Test,
      handlebars,
      playMailer,
      playMailerGuice,
      pbkdf2,
      commonCodec,
      scalaGuice,
      reflections,
      quartzScheduler
    )
  )

lazy val cynoxDto = (project in file("dto"))
  .dependsOn(scalligraph)
  .settings(
    name := "cynox-dto",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      aix
    )
  )

lazy val cynoxClient = (project in file("client"))
  .dependsOn(cynoxDto)
  .dependsOn(clientCommon)
  .settings(
    name := "cynox-client",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      ws
    )
  )

lazy val npm        = taskKey[Unit]("Install npm dependencies")
lazy val bower      = taskKey[Unit]("Install bower dependencies")
lazy val gruntDev   = taskKey[Unit]("Inject bower dependencies in index.html")
lazy val gruntBuild = taskKey[Seq[(File, String)]]("Build frontend files")

lazy val cynoxFrontend = (project in file("frontend"))
  .settings(
    name := "cynox-frontend",
    version := cynoxVersion,
    npm :=
      FileBuilder(
        label = "npm",
        inputFiles = baseDirectory.value / "package.json",
        outputFiles = baseDirectory.value / "node_modules" ** AllPassFilter,
        command = baseDirectory.value -> "npm install",
        streams = streams.value
      ),
    bower := FileBuilder(
      label = "bower",
      inputFiles = baseDirectory.value / "bower.json",
      outputFiles = baseDirectory.value / "bower_components" ** AllPassFilter,
      command = baseDirectory.value -> "bower install",
      streams = streams.value
    ),
    gruntDev := {
      npm.value
      bower.value
      FileBuilder(
        label = "grunt",
        inputFiles = baseDirectory.value / "bower_components" ** AllPassFilter,
        outputFiles = baseDirectory.value / "app" / "index.html",
        command = baseDirectory.value -> "grunt wiredep",
        streams = streams.value
      )
    },
    gruntBuild := {
      npm.value
      bower.value
      val dist = baseDirectory.value / "dist"
      val outputFiles = FileBuilder(
        label = "grunt",
        inputFiles = baseDirectory.value / "bower_components" ** AllPassFilter,
        outputFiles = dist ** AllPassFilter,
        command = baseDirectory.value -> "grunt build",
        streams = streams.value
      )
      for {
        file        <- outputFiles.toSeq
        rebasedFile <- sbt.Path.rebase(dist, "frontend")(file)
      } yield file -> rebasedFile
    },
    Compile / resourceDirectory := baseDirectory.value / "app",
    Compile / packageBin / mappings := gruntBuild.value,
    watchSources := Nil,
    cleanFiles ++= Seq(
      baseDirectory.value / "dist",
      baseDirectory.value / "bower_components",
      baseDirectory.value / "node_modules"
    )
  )

lazy val clientCommon = (project in file("client-common"))
  .dependsOn(scalligraph)
  .settings(
    name := "client-common",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      ws,
      specs % Test
    )
  )

lazy val cynoxCortex = (project in file("cortex/connector"))
  .dependsOn(cynoxCore)
  .dependsOn(cortexClient)
  .dependsOn(cortexClient % "test -> test")
  .dependsOn(cynoxCore % "test -> test")
  .dependsOn(scalligraph % "test -> test")
  .settings(
    name := "cynox-cortex",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      reflections,
      specs % Test
    )
  )

lazy val cortexDto = (project in file("cortex/dto"))
  .dependsOn(scalligraph)
  .settings(
    name := "cortex-dto",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      chimney
    )
  )

lazy val cortexClient = (project in file("cortex/client"))
  .dependsOn(cortexDto)
  .dependsOn(clientCommon)
  .dependsOn(scalligraph % "test -> test")
  .settings(
    name := "cortex-client",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      ws,
      specs            % Test,
      playFilters      % Test,
      playMockws       % Test,
      akkaClusterTyped % Test
    )
  )

lazy val cynoxMisp = (project in file("misp/connector"))
  .dependsOn(cynoxCore)
  .dependsOn(mispClient)
  .dependsOn(cynoxCore % "test -> test")
  .settings(
    name := "cynox-misp",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      specs      % Test,
      playMockws % Test
    )
  )

lazy val mispClient = (project in file("misp/client"))
  .dependsOn(scalligraph)
  .dependsOn(clientCommon)
  .settings(
    name := "misp-client",
    version := cynoxVersion,
    libraryDependencies ++= Seq(
      ws,
      alpakka,
      akkaHttp,
      specs      % Test,
      playMockws % Test
    )
  )

lazy val cynoxMigration = (project in file("migration"))
  .enablePlugins(JavaAppPackaging)
  .dependsOn(scalligraph)
  .dependsOn(cynoxCore)
  .dependsOn(cynoxCortex)
  .settings(
    name := "cynox-migration",
    version := cynoxVersion,
    resolvers += "elasticsearch-releases" at "https://artifacts.elastic.co/maven",
    crossScalaVersions := Seq(scala212),
    libraryDependencies ++= Seq(
      alpakka,
      ehcache,
      scopt,
      specs % Test
    ),
    normalizedName := "migrate"
  )
