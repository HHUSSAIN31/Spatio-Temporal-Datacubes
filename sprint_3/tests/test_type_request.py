import unittest
from src.type_request import type_request


class dbc_tester(unittest.TestCase):
    def test_type_request_param(self):
        """Testing the behaivor of creating a type_request object."""
        failing_lst_for_exp_str = [-1, 1, 1.32, (1, 2), {}, []]
        failing_lst_for_exp_lst = [-1, 1, 1.32, (1, 2), {}, ""]

        for test_case in failing_lst_for_exp_str:
            try:
                type_request(id=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_str:
            try:
                type_request(coverageType=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_str:
            try:
                type_request(service_endpoint=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_str:
            try:
                type_request(serviceType=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_str:
            try:
                type_request(serviceVersion=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_str:
            try:
                type_request(request=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")


        for test_case in failing_lst_for_exp_lst:
            try:
                type_request(bounds_1=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_lst:
            try:
                type_request(bounds_2=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_lst:
            try:
                type_request(additionalParameters=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_for_exp_lst:
            try:
                type_request(coverageTypeExtended=test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

    def test_type_request_comparison(self):
        """Testing the comaprison behaivor of type_request objects."""
        failing_lst_types = [-1, 1, 1.32, (1, 2), {}, [], ""]
        dummy_1 = type_request(id="me")
        dummy_2 = type_request(id="you")

        for test_case in failing_lst_types:
            try:
                test_case > dummy_1
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

            try:
                test_case >= dummy_1
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

            try:
                test_case == dummy_1
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

            try:
                test_case < dummy_1
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

            try:
                test_case <= dummy_1
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        if dummy_1 == dummy_2:
            self.fail(f"test case: == failed.")
        elif dummy_1 > dummy_2:
            self.fail(f"test case: > failed.")
        elif dummy_1 >= dummy_2:
            self.fail(f"test case: >= failed.")
        elif dummy_1 < dummy_2 or dummy_1 <= dummy_2:
            pass

        if dummy_2 == dummy_1:
            self.fail(f"test case: == failed.")
        elif dummy_2 < dummy_1:
            self.fail(f"test case: > failed.")
        elif dummy_2 <= dummy_1:
            self.fail(f"test case: >= failed.")
        elif dummy_2 > dummy_1 or dummy_2 >= dummy_1:
            pass


if __name__ == '__main__':
    unittest.main()
