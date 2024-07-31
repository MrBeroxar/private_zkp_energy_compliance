import json


class ZokInputGenerator:
    def __init__(self, consumption, production, netResult, signatures, public_key):
        self.consumption = consumption
        self.production = production
        self.netResult = netResult
        self.signatures = signatures
        self.public_key = public_key

    def generate_json_output(self):
        json_output = []
        for sig in self.signatures:
            json_output.extend(
                [
                    [str(sig[0].x.n), str(sig[0].y.n)],
                    str(sig[1]),
                ]
            )
        json_output.extend(
            [
                [str(self.public_key.point.x.n), str(self.public_key.point.y.n)],
                [str(x) for x in self.consumption],
                [str(x) for x in self.production],
                str(self.netResult),
            ]
        )
        # print(json.dumps(json_output, indent=2))
        return json.dumps(json_output, indent=2)
