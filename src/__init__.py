from mock_meter.GaussianMockDataGenerator import GaussianMockDataGenerator
from mock_meter.SignatureGenerator import SignatureGenerator
from mock_meter.ZokInputGenerator import ZokInputGenerator


def main():
    generator = GaussianMockDataGenerator(array_size=16)
    consumption, production, netResult = generator.get_gaussian_mock_data(
        consumption_mean=10, production_mean=4
    )

    signer = SignatureGenerator(consumption, production)
    signatures, pk = signer.sign_parts(parts=len(consumption) // 8)

    json_generator = ZokInputGenerator(
        consumption, production, netResult, signatures, pk
    )
    json_str = json_generator.generate_json_output()
    # print(json_str)


if __name__ == "__main__":
    main()
