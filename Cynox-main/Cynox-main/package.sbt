import Common.remapPath
// Remove conf files
// Install service files
mappings in Universal ~= {
  _.flatMap {
    case (_, "conf/application.conf")           => Nil
    case (file, "conf/application.sample.conf") => Seq(file -> "conf/application.conf")
    case (_, "conf/logback.xml")                => Nil
    case (_, "conf/logback-migration.xml")      => Nil
    case other                                  => Seq(other)
  } ++ Seq(
    file("package/logback.xml")           -> "conf/logback.xml",
    file("package/logback-migration.xml") -> "conf/logback-migration.xml"
  )
}

// Package //
packageName := "cynox4"
maintainer := "Cynox Project <support@cynox-project.org>"
packageSummary := "Scalable, Open Source and Free Security Incident Response Solutions"
packageDescription :=
  """Cynox is a scalable 3-in-1 open source and free security incident response
    | platform designed to make life easier for SOCs, CSIRTs, CERTs and any
    | information security practitioner dealing with security incidents that need to
    | be investigated and acted upon swiftly.""".stripMargin
defaultLinuxInstallLocation := "/opt"
linuxPackageMappings ~= {
  _.map { pm =>
    val mappings = pm
      .mappings
      .map(remapPath("cynox4", "cynox", "/etc", "/opt", "/var/log"))
      .filterNot {
        case (_, path) => path.startsWith("/opt/cynox/conf") || path.startsWith("/usr/bin")
      }
    com.typesafe.sbt.packager.linux.LinuxPackageMapping(mappings, pm.fileData)
  }
}
linuxPackageMappings ++= Seq(
  packageMapping(
    file("package/cynox.service") -> "/usr/lib/systemd/system/cynox.service"
  ).withPerms("644"),
  packageMapping(
    file("package/cynox.default")       -> "/etc/default/cynox",
    file("conf/application.sample.conf")  -> "/etc/cynox/application.conf",
    file("package/logback.xml")           -> "/etc/cynox/logback.xml",
    file("package/logback-migration.xml") -> "/etc/cynox/logback-migration.xml"
  ).withPerms("644").withConfig()
)
daemonUser := "cynox"
bashScriptEnvConfigLocation := None
