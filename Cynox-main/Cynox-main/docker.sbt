import Common.{betaVersion, snapshotVersion, stableVersion, versionUsage}
import com.typesafe.sbt.packager.docker.{Cmd, ExecCmd}

version in Docker := {
  version.value match {
    case stableVersion(_, _)                      => version.value
    case betaVersion(v1, v2, v3)                  => v1 + "-0." + v3 + "RC" + v2
    case snapshotVersion(stableVersion(v1, v2))   => v1 + "-" + v2 + "-SNAPSHOT"
    case snapshotVersion(betaVersion(v1, v2, v3)) => v1 + "-0." + v3 + "RC" + v2 + "-SNAPSHOT"
    case _                                        => versionUsage(version.value)
  }
}
defaultLinuxInstallLocation in Docker := "/opt/cynox"
dockerRepository := Some("cynoxproject")
dockerUpdateLatest := !version.value.toUpperCase.contains("RC") && !version.value.contains("SNAPSHOT")
dockerExposedPorts := Seq(9000)
mappings in Docker ++= Seq(
  file("package/docker/entrypoint")     -> "/opt/cynox/entrypoint",
  file("package/logback.xml")           -> "/etc/cynox/logback.xml",
  file("package/logback-migration.xml") -> "/etc/cynox/logback-migration.xml",
  file("package/empty")                 -> "/var/log/cynox/application.log"
)
mappings in Docker ~= (_.filterNot {
  case (_, filepath) => filepath == "/opt/cynox/conf/application.conf"
})
dockerCommands := Seq(
  Cmd("FROM", "openjdk:8"),
  Cmd("LABEL", "MAINTAINER=\"Cynox Project <support@cynox-project.org>\""),
  Cmd("WORKDIR", "/opt/cynox"),
  // format: off
  Cmd("RUN",
    "apt", "update", "&&",
    "apt", "upgrade", "-y", "&&",
    "apt", "autoclean", "-y", "-q",  "&&",
    "apt", "autoremove", "-y", "-q",  "&&",
    "rm", "-rf", "/var/lib/apt/lists/*", "&&",
    "(", "type", "groupadd", "1>/dev/null", "2>&1", "&&",
      "groupadd", "-g", "1000", "cynox", "||",
      "addgroup", "-g", "1000", "-S", "cynox",
    ")", "&&",
    "(", "type", "useradd", "1>/dev/null", "2>&1", "&&",
      "useradd", "--system", "--uid", "1000", "--gid", "1000", "cynox", "||",
      "adduser", "-S", "-u", "1000", "-G", "cynox", "cynox",
    ")"),
  //format: on
  Cmd("ADD", "--chown=root:root", "opt", "/opt"),
  Cmd("ADD", "--chown=cynox:cynox", "var", "/var"),
  Cmd("ADD", "--chown=cynox:cynox", "etc", "/etc"),
  ExecCmd("RUN", "chmod", "+x", "/opt/cynox/bin/cynox", "/opt/cynox/entrypoint", "/opt/cynox/bin/cloner", "/opt/cynox/bin/migrate"),
  Cmd("RUN", "mkdir", "/data", "/opt/thp", "&&", "chown", "cynox:cynox", "/data", "/opt/thp"),
  Cmd("EXPOSE", "9000"),
  Cmd("USER", "cynox"),
  ExecCmd("ENTRYPOINT", "/opt/cynox/entrypoint"),
  ExecCmd("CMD")
)
