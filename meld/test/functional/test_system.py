import unittest
from meld.system import protein, builder, ConstantTemperatureScaler, LinearTemperatureScaler
from meld.system import GeometricTemperatureScaler


class TestCreateFromSequence(unittest.TestCase):
    def setUp(self):
        p = protein.ProteinMoleculeFromSequence('NALA ALA CALA')
        b = builder.SystemBuilder()
        self.system = b.build_system_from_molecules([p])

    def test_has_correct_number_of_atoms(self):
        self.assertEqual(self.system.n_atoms, 33)

    def test_coordinates_have_correct_shape(self):
        self.assertEqual(self.system.coordinates.shape[0], 33)
        self.assertEqual(self.system.coordinates.shape[1], 3)

    def test_has_correct_atom_names(self):
        self.assertEqual(self.system.atom_names[0], 'N')
        self.assertEqual(self.system.atom_names[-1], 'OXT')
        self.assertEqual(len(self.system.atom_names), self.system.coordinates.shape[0])

    def test_has_correct_residue_indices(self):
        self.assertEqual(self.system.residue_numbers[0], 1)
        self.assertEqual(self.system.residue_numbers[-1], 3)
        self.assertEqual(len(self.system.residue_numbers), self.system.coordinates.shape[0])

    def test_has_correct_residue_names(self):
        self.assertEqual(self.system.residue_names[0], 'ALA')
        self.assertEqual(self.system.residue_names[-1], 'ALA')
        self.assertEqual(len(self.system.residue_names), self.system.coordinates.shape[0])

    def test_index_works(self):
        self.assertEqual(self.system.index_of_atom(1, 'N'), 1)
        self.assertEqual(self.system.index_of_atom(3, 'OXT'), 33)

    def test_temperature_scaler_defaults_to_none(self):
        self.assertEqual(self.system.temperature_scaler, None)


class TestConstantTemperatureScaler(unittest.TestCase):
    def setUp(self):
        self.s = ConstantTemperatureScaler(300.)

    def test_returns_constant_when_alpha_is_zero(self):
        t = self.s(0.)
        self.assertAlmostEqual(t, 300.)

    def test_returns_constant_when_alpha_is_one(self):
        t = self.s(1.)
        self.assertAlmostEqual(t, 300.)

    def test_raises_when_alpha_below_zero(self):
        with self.assertRaises(RuntimeError):
            self.s(-1)

    def test_raises_when_alpha_above_one(self):
        with self.assertRaises(RuntimeError):
            self.s(2)


class TestLinearTemperatureScaler(unittest.TestCase):
    def setUp(self):
        self.s = LinearTemperatureScaler(0.2, 0.8, 300., 500.)

    def test_returns_min_when_alpha_is_low(self):
        t = self.s(0)
        self.assertAlmostEqual(t, 300.)

    def test_returns_max_when_alpha_is_high(self):
        t = self.s(1)
        self.assertAlmostEqual(t, 500.)

    def test_returns_mid_when_alpha_is_half(self):
        t = self.s(0.5)
        self.assertAlmostEqual(t, 400.)

    def test_raises_when_alpha_below_zero(self):
        with self.assertRaises(RuntimeError):
            self.s(-1)

    def test_raises_when_alpha_above_one(self):
        with self.assertRaises(RuntimeError):
            self.s(2)

    def test_raises_when_alpha_min_below_zero(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(-0.1, 0.8, 300., 500.)

    def test_raises_when_alpha_min_above_one(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(1.1, 0.8, 300., 500.)

    def test_raises_when_alpha_max_below_zero(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(0.0, -0.1, 300., 500.)

    def test_raises_when_alpha_max_above_one(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(0.0, 1.1, 300., 500.)

    def test_raises_when_alpha_min_above_alpha_max(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(1.0, 0.0, 300., 500.)

    def test_raises_when_temp_min_is_below_zero(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(0.0, 1.0, -300., 500.)

    def test_raises_when_temp_max_is_below_zero(self):
        with self.assertRaises(RuntimeError):
            LinearTemperatureScaler(0.0, 1.0, 300., -500.)


class TestGeometricTemperatureScaler(unittest.TestCase):
    def setUp(self):
        self.s = GeometricTemperatureScaler(0.2, 0.8, 300., 500.)

    def test_returns_min_when_alpha_is_low(self):
        t = self.s(0)
        self.assertAlmostEqual(t, 300.)

    def test_returns_max_when_alpha_is_high(self):
        t = self.s(1)
        self.assertAlmostEqual(t, 500.)

    def test_returns_mid_when_alpha_is_half(self):
        t = self.s(0.5)
        self.assertAlmostEqual(t, 387.298334621)

    def test_raises_when_alpha_below_zero(self):
        with self.assertRaises(RuntimeError):
            self.s(-1)

    def test_raises_when_alpha_above_one(self):
        with self.assertRaises(RuntimeError):
            self.s(2)

    def test_raises_when_alpha_min_below_zero(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(-0.1, 0.8, 300., 500.)

    def test_raises_when_alpha_min_above_one(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(1.1, 0.8, 300., 500.)

    def test_raises_when_alpha_max_below_zero(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(0.0, -0.1, 300., 500.)

    def test_raises_when_alpha_max_above_one(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(0.0, 1.1, 300., 500.)

    def test_raises_when_alpha_min_above_alpha_max(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(1.0, 0.0, 300., 500.)

    def test_raises_when_temp_min_is_below_zero(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(0.0, 1.0, -300., 500.)

    def test_raises_when_temp_max_is_below_zero(self):
        with self.assertRaises(RuntimeError):
            GeometricTemperatureScaler(0.0, 1.0, 300., -500.)
