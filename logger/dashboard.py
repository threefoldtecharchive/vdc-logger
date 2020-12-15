dashboard_json = """
{
"dashboard": {
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "datasource": null,
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "id": 4,
      "options": {
        "showLabels": false,
        "showTime": false,
        "sortOrder": "Descending",
        "wrapLogMessage": false
      },
      "pluginVersion": "7.3.4",
      "targets": [
        {
          "groupBy": [],
          "measurement": "alerts",
          "orderByTime": "ASC",
          "policy": "default",
          "refId": "A",
          "resultFormat": "logs",
          "select": [
            [
              {
                "params": [
                  "message"
                ],
                "type": "field"
              }
            ]
          ],
          "tags": [
            {
              "key": "tname",
              "operator": "=",
              "value": "{tname}"
            },
            {
              "condition": "AND",
              "key": "vdc_name",
              "operator": "=",
              "value": "{vdcname}"
            },
            {
              "condition": "AND",
              "key": "explorer",
              "operator": "=",
              "value": "{explorer}"
            }
          ]
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "Alerts",
      "type": "logs"
    },
    {
      "datasource": null,
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 0
      },
      "id": 6,
      "options": {
        "showLabels": false,
        "showTime": false,
        "sortOrder": "Descending",
        "wrapLogMessage": false
      },
      "pluginVersion": "7.3.4",
      "targets": [
        {
          "groupBy": [],
          "measurement": "logs",
          "orderByTime": "ASC",
          "policy": "default",
          "refId": "A",
          "resultFormat": "logs",
          "select": [
            [
              {
                "params": [
                  "message"
                ],
                "type": "field"
              }
            ]
          ],
          "tags": [
            {
              "key": "tname",
              "operator": "=",
              "value": "{tname}"
            },
            {
              "condition": "AND",
              "key": "vdc_name",
              "operator": "=",
              "value": "{vdcname}"
            },
            {
              "condition": "AND",
              "key": "explorer",
              "operator": "=",
              "value": "{explorer}"
            }
          ]
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "Threebot logs",
      "type": "logs"
    },
    {
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "InfluxDB",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 9,
        "w": 12,
        "x": 0,
        "y": 8
      },
      "hiddenSeries": false,
      "id": 2,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.4",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "groupBy": [
            {
              "params": [
                "20s"
              ],
              "type": "time"
            },
            {
              "params": [
                "0"
              ],
              "type": "fill"
            }
          ],
          "measurement": "heartbeats",
          "orderByTime": "ASC",
          "policy": "default",
          "refId": "A",
          "resultFormat": "time_series",
          "select": [
            [
              {
                "params": [
                  "exists"
                ],
                "type": "field"
              },
              {
                "params": [],
                "type": "mean"
              }
            ]
          ],
          "tags": [
            {
              "key": "vdc_name",
              "operator": "=",
              "value": "{vdcname}"
            },
            {
              "condition": "AND",
              "key": "tname",
              "operator": "=",
              "value": "{tname}"
            },
            {
              "condition": "AND",
              "key": "explorer",
              "operator": "=",
              "value": "{explorer}"
            }
          ]
        }
      ],
      "thresholds": [],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Hearbeats",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    }
  ],
  "schemaVersion": 26,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-30m",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "{tname}-{vdcname}",
  "uid": null,
  "version": 4
}
}
"""

def get_dashboard_json(tname, vdcname, explorer):
    x = dashboard_json
    x = x.replace("{tname}", tname)
    x = x.replace("{vdcname}", vdcname)
    x = x.replace("{explorer}", explorer)
    return x
