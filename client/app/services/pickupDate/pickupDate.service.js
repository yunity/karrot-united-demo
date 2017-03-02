class PickupDateComService {
  constructor($http) {
    "ngInject";
    this.$http = $http;
  }

  create(pickup) {
    return this.$http.post("/api/pickup-dates/", this.$serialize(pickup))
      .then((res) => this.$parse(res.data));
  }

  get(pickupId) {
    return this.$http.get(`/api/pickup-dates/${pickupId}/`)
      .then((res) => this.$parse(res.data));
  }

  list() {
    return this.$http.get("/api/pickup-dates/", { params: { "date_0": new Date() } })
      .then((res) => this.$parseList(res.data));
  }

  listByGroupId(groupId) {
    return this.$http.get("/api/pickup-dates/", { params: { group: groupId, "date_0": new Date() } })
      .then((res) => this.$parseList(res.data));
  }

  listByStoreId(storeId) {
    return this.$http.get("/api/pickup-dates/", { params: { store: storeId, "date_0": new Date() } })
      .then((res) => this.$parseList(res.data));
  }

  save(pickup) {
    let pickupId = pickup.id;
    return this.$http.patch(`/api/pickup-dates/${pickupId}/`, this.$serialize(pickup))
      .then((res) => this.$parse(res.data));
  }

  delete(pickupId) {
    return this.$http.delete(`/api/pickup-dates/${pickupId}/`);
  }

  join(pickupId) {
    return this.$http.post(`/api/pickup-dates/${pickupId}/add/`, {})
      .then((res) => this.$parse(res.data));
  }

  leave(pickupId) {
    return this.$http.post(`/api/pickup-dates/${pickupId}/remove/`, {})
      .then((res) => this.$parse(res.data));
  }

  // conversion methods for this service

  $parse(external) {
    Object.assign(external, {
      date: new Date(external.date),
      maxCollectors: external.max_collectors
    });
    delete external.max_collectors;
    return external;
  }

  $parseList(external) {
    angular.forEach(external, (entry) => {
      this.$parse(entry);
    });
    return external;
  }

  $serialize(internal) {
    Object.assign(internal, {
      "max_collectors": internal.maxCollectors
    });
    delete internal.maxCollectors;
    return internal;
  }
}

export default PickupDateComService;
