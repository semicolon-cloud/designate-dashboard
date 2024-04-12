/**
 *
 * (c) Copyright 2016 Hewlett Packard Enterprise Development Company LP
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function () {
  'use strict';

  angular
    .module('designatedashboard.resources.os-designate-zone.actions')
    .factory('designatedashboard.resources.os-designate-zone.actions.request', action);

  action.$inject = [
    '$q',
    'designatedashboard.resources.os-designate-zone.actions.common-forms',
    'designatedashboard.resources.os-designate-zone.api',
    'designatedashboard.resources.os-designate-zone.resourceType',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.serviceCatalog',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service'
  ];

  /*
   * @ngDoc factory
   * @name designatedashboard.resources.os-designate-zone.actions.create
   *
   * @Description
   * Brings up the Create Zone modal.
   */
  function action($q,
                  forms,
                  api,
                  resourceTypeName,
                  policy,
                  serviceCatalog,
                  schemaFormModalService,
                  toast,
                  waitSpinner) {
    var createZonePolicy, dnsServiceEnabled;
    var title = gettext("Request Zone");
    var message = {
      success: gettext('Zone %s was successfully requested to be created.')
    };

    var service = {
      initAction: initAction,
      allowed: allowed,
      perform: perform
    };

    return service;

    /////////////////

    function initAction() {
      dnsServiceEnabled = serviceCatalog.ifTypeEnabled('dns');
    }

    function allowed() {
      return $q.all([
        dnsServiceEnabled
      ]);
    }

    function perform() {
      var formConfig = forms.getRequestFormConfig();
      formConfig.title = title;
      return schemaFormModalService.open(formConfig).then(onSubmit, onCancel);
    }

    function onSubmit(context) {
      var zoneModel = angular.copy(context.model);

      waitSpinner.showModalSpinner(gettext('Requesting to request Zone'));

      return api.request_creation(zoneModel).then(onSuccess, onFailure);
    }

    function onCancel() {
      waitSpinner.hideModalSpinner();
    }

    function onSuccess(response) {
      waitSpinner.hideModalSpinner();
      var zone = response.data;
      toast.add('success', interpolate(message.success, [zone.name]));

      // To make the result of this action generically useful, reformat the return
      // from the deleteModal into a standard form
      return {
        created: [{type: resourceTypeName, id: zone.id}],
        updated: [],
        deleted: [],
        failed: []
      };
    }

    function onFailure() {
      waitSpinner.hideModalSpinner();
    }
  }
})();