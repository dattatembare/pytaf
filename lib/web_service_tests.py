def add_web_service_tests():
    def assertWebServiceErrorResponse(self, response, code=None, event_type=None, description=None,
                                      resolution=None):
        data = self.assertWebServiceResponse(response)

        self.assertEqual(len(data['errors']), 1)
        error = data['errors'][0]
        self.assertIsNotNone(data['errors'][0])
        if code is not None:
            self.assertEqual(error['code'], code)
        if event_type is not None:
            self.assertEqual(error['eventType'], event_type)
        if description is not None:
            self.assertEqual(error['description'], description)
        if resolution is not None:
            self.assertEqual(error['resolution'], resolution)

        return error

    def assertWebServiceResponse(self, response):
        self.assertIsNotNone(response)

        data = response.data
        self.assertIsNotNone(data)
        self.assertIsNotNone(data['id'])
        self.assertIsNotNone(data['timestamp'])
        return data

    def _decorator(cls):
        cls.assertWebServiceErrorResponse = assertWebServiceErrorResponse
        cls.assertWebServiceResponse = assertWebServiceResponse
        return cls

    return _decorator
