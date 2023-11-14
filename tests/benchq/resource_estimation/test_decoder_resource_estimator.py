import os
import warnings

import pytest

from benchq.data_structures import (
    BASIC_SC_ARCHITECTURE_MODEL,
    DecoderInfo,
    DecoderModel,
)
from benchq.resource_estimation.decoder_resource_estimator import get_decoder_info


def file_path(file_name):
    curent_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(curent_dir, file_name)


def test_none_decoder_model_returns_non_decoder_info():
    assert get_decoder_info(BASIC_SC_ARCHITECTURE_MODEL, None, 1, 2, 3) is None


@pytest.mark.parametrize(
    "distance, expected_warning_message, decoder_data",
    [
        (17, "the decoder is too slow", "decoder_test_data_speed_limited"),
        (
            32,
            "resource estimates have not been calculated",
            "decoder_test_data_size_limited",
        ),
    ],
)
def test_decoder_model_produces_none_and_throws_warning_for_distance_too_high(
    distance, expected_warning_message, decoder_data
):
    decoder_model = DecoderModel.from_csv(file_path(decoder_data + ".csv"))
    with warnings.catch_warnings(record=True) as w:
        assert (
            get_decoder_info(BASIC_SC_ARCHITECTURE_MODEL, decoder_model, distance, 2, 3)
            is None
        )

        assert len(w) == 1
        assert issubclass(w[0].category, RuntimeWarning)
        assert expected_warning_message in str(w[0].message)


def test_if_decoder_equations_have_changed():
    decoder_model = DecoderModel.from_csv(
        file_path("decoder_test_data_speed_limited.csv")
    )
    decoder_info = get_decoder_info(BASIC_SC_ARCHITECTURE_MODEL, decoder_model, 4, 2, 3)
    target_info = DecoderInfo(
        total_energy_consumption_in_nanojoules=0.004,
        power_in_nanowatts=120000.0,
        area_in_micrometers_squared=600.0,
        max_decodable_distance=15,
    )
    print(decoder_info)
    print(decoder_info.max_decodable_distance)

    assert target_info == decoder_info