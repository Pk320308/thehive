# References to "Cynox" (and Variations)

This document contains a structured summary of all occurrences of **Cynox**, **cynox**, **Cynox**, **Cynox**, and **CYNOX** in the codebase. 

A complete list of all **528 occurrences** has been compiled and saved to the CSV file at [cynox_occurrences.csv](file:///E:/THE%20Hive%20New/cynox_occurrences.csv). You can open this file in Excel or Notepad to see the exact line numbers and matches.

---

## 📂 Category Breakdown

### 1. Automation & Backup Scripts (13 Files)
These scripts contain path configurations, comments, and task scheduler descriptions where "Cynox" is referenced.

| File | Primary Use of "Cynox" / Context |
| :--- | :--- |
| [auto_backup.ps1](file:///E:/THE%20Hive%20New/auto_backup.ps1) | References to Cassandra, Elasticsearch, and Cynox db directories. |
| [backup_cynox.ps1](file:///E:/THE%20Hive%20New/backup_cynox.ps1) | Console logging and folder paths. |
| [cynox_autorefresh.user.js](file:///E:/THE%20Hive%20New/cynox_autorefresh.user.js) | Userscript name and description metadata. |
| [cynox_backup_task.xml](file:///E:/THE%20Hive%20New/cynox_backup_task.xml) | Task Scheduler registration descriptions and arguments. |
| [cynox_health_task.xml](file:///E:/THE%20Hive%20New/cynox_health_task.xml) | Health monitor task description. |
| [health_monitor.ps1](file:///E:/THE%20Hive%20New/health_monitor.ps1) | Logging statements and health check comments. |
| [inject_autorefresh.py](file:///E:/THE%20Hive%20New/inject_autorefresh.py) | JAR path and script injection markers. |
| [inject_autorefresh.sh](file:///E:/THE%20Hive%20New/inject_autorefresh.sh) | Shell injector JAR references. |
| [reset.sh](file:///E:/THE%20Hive%20New/reset.sh) | Admin credentials check (`admin@thehive.local`). |
| [reset_pass.ps1](file:///E:/THE%20Hive%20New/reset_pass.ps1) | Default admin user email (`admin@thehive.local`). |
| [restore_cynox.ps1](file:///E:/THE%20Hive%20New/restore_cynox.ps1) | Script description and terminal output strings. |
| [test_login.sh](file:///E:/THE%20Hive%20New/test_login.sh) | Default login API test payload. |
| [backup_log.txt](file:///E:/THE%20Hive%20New/BACKUPS/backup_log.txt) | Automatic backup file path logs. |

---

### 2. Configuration & Deployment (1 File)
Standard docker environment references and mounts.

| File | Occurrences | Context / Example |
| :--- | :---: | :--- |
| [docker-compose.yml](file:///E:/THE%20Hive%20New/docker-compose.yml) | 4 | Docker image `cynoxproject/cynox4` and path mount volumes. |

---

### 3. Backend Source Code (Scala) (25 Files)
Core backend logic, MISP and Cortex integrations, test files, and package configurations.

| File Group | Files | Description / Examples |
| :--- | :--- | :--- |
| **SBT Build Specs** | [build.sbt](file:///E:/THE%20Hive%20New/build.sbt), [debian.sbt](file:///E:/THE%20Hive%20New/debian.sbt), [docker.sbt](file:///E:/THE%20Hive%20New/docker.sbt), [package.sbt](file:///E:/THE%20Hive%20New/package.sbt) | Module names (`cynoxVersion`, `cynoxCore`, `cynoxFrontend`, package target `cynox4`). |
| **Configs** | [application.conf](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/conf/application.conf), [application.sample.conf](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/conf/application.sample.conf), [reference-overrides.conf](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/conf/reference-overrides.conf) | Keyspace configurations, index names, local filesystem locations, module references (`org.thp.cynox.CynoxModule`). |
| **Cortex Connectors** | [CortexClient.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cortex/connector/src/main/scala/org/thp/cynox/connector/cortex/services/CortexClient.scala), [CortexModule.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cortex/connector/src/main/scala/org/thp/cynox/connector/cortex/CortexModule.scala), [CynoxCortexSchemaProvider.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cortex/connector/src/main/scala/org/thp/cynox/connector/cortex/models/CynoxCortexSchemaProvider.scala), [Connector.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cortex/connector/src/main/scala/org/thp/cynox/connector/cortex/services/Connector.scala) | Variable names (`includedCynoxOrganisations`), classes, imports. |
| **MISP Connectors** | [MispModule.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/misp/connector/src/main/scala/org/thp/cynox/connector/misp/MispModule.scala), [MispExportSrv.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/misp/connector/src/main/scala/org/thp/cynox/connector/misp/services/MispExportSrv.scala), [MispImportSrv.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/misp/connector/src/main/scala/org/thp/cynox/connector/misp/services/MispImportSrv.scala), [CynoxMispClient.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/misp/connector/src/main/scala/org/thp/cynox/connector/misp/services/CynoxMispClient.scala) | Classes (`CynoxMispClientConfig`, `CynoxMispClient`), variable names. |
| **Core Backend & Routing** | [CynoxModule.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/CynoxModule.scala), [CynoxRouter.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/CynoxRouter.scala), [Router.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/controllers/v1/Router.scala), [StatusCtrl.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/controllers/v1/StatusCtrl.scala), [CynoxQueryExecutor.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/controllers/v0/CynoxQueryExecutor.scala), [Permissions.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/models/Permissions.scala), [CynoxSchemaDefinition.scala](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/cynox/src/main/scala/org/thp/cynox/models/CynoxSchemaDefinition.scala) | Permissions definitions (`accessCynoxFS`), schema definitions, controllers. |
| **Backend Unit Tests** | `*Test.scala` (multiple files) | Integration and unit tests mimicking backend components (e.g. `JobCtrlTest.scala`, `ActionSrvTest.scala`, `StatusCtrlTest.scala`). |

---

### 4. Frontend AngularJS Code (178 Files)
Almost every file in the frontend AngularJS codebase references `cynox` as part of module namespace definitions (e.g., `cynoxControllers`, `cynoxServices`, `cynoxFilters`, `cynoxDirectives`, `cynoxComponents`).

* **Modules Declarations & Setup**:
  * [app.js](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/frontend/src/app.js)
  * [app-container.component.js](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/frontend/src/app-container.component.js)
* **Directives & Components**:
  * Over 150 component files referencing services under `angular.module('cynoxComponents')` or `angular.module('cynoxControllers')`.
* **Templates**:
  * [header.component.html](file:///E:/THE%20Hive%20New/Cynox-main/Cynox-main/frontend/src/header.component.html) contains `<a href ng-click="aboutCynox()">` references.

---

### 5. Documentation & Project Info (4 Files)
* [CHANGELOG.md](file:///E:/THE%20Hive%20New/CHANGELOG.md) - History logs referencing old version issues and pull request links.
* [cynox3_bug_report.md](file:///E:/THE%20Hive%20New/.github/ISSUE_TEMPLATE/cynox3_bug_report.md) - Github issue tracker files.
* [cynox4_bug_report.md](file:///E:/THE%20Hive%20New/.github/ISSUE_TEMPLATE/cynox4_bug_report.md)
* [cynox4_feature_request.md](file:///E:/THE%20Hive%20New/.github/ISSUE_TEMPLATE/cynox4_feature_request.md)

---

## 💡 Recommendation
Since there are **528 references** spanning configuration files, code directories, and internal AngularJS namespaces, attempting to rename all of them manually could break the internal Javascript logic and compilation bindings. If your goal is to brand the UI as **Cynox**, the recommended approach is:
1. Focus on modifying visible title strings, logos, and frontend templates rather than renaming the internal variable namespaces (`cynoxControllers`, etc.) which might cause run-time crash bugs.
2. We have already completed major branding changes on the visible areas. Let us know if you want us to adjust any specific labels!
