#!/pxrpythonsubst
#
# Copyright 2026 Pixar
#
# Licensed under the terms set forth in the LICENSE.txt file available at
# https://openusd.org/license.

import unittest
from pxr import Usd, UsdVol


class TestUsdVolParticleField(unittest.TestCase):

    _ColorSpaceNameFallback = "srgb_rec709_display"

    def _VerifyColorSpaceNameFallback(self, prim):
        attrAPI = UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI(prim)

        self.assertTrue(
            callable(getattr(attrAPI, "GetColorSpaceNameAttr", None)))
        self.assertTrue(
            callable(getattr(attrAPI, "CreateColorSpaceNameAttr", None)))

        colorSpaceNameAttr = attrAPI.GetColorSpaceNameAttr()
        self.assertTrue(colorSpaceNameAttr)
        self.assertEqual(colorSpaceNameAttr.Get(),
                         self._ColorSpaceNameFallback)

    def test_SphericalHarmonicsColorSpaceFallback(self):
        stage = Usd.Stage.CreateInMemory("particleField.usda")

        particleField = UsdVol.ParticleField.Define(stage, "/ParticleField")
        attrAPI = UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI.Apply(
            particleField.GetPrim())
        self.assertTrue(attrAPI)

        particleFieldPrim = particleField.GetPrim()
        self.assertTrue(particleFieldPrim.HasAPI(
            UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI))
        self.assertIn("ParticleFieldSphericalHarmonicsAttributeAPI",
                      particleFieldPrim.GetAppliedSchemas())
        self._VerifyColorSpaceNameFallback(particleFieldPrim)

        gaussianSplat = UsdVol.ParticleField3DGaussianSplat.Define(
            stage, "/GaussianSplat")
        gaussianSplatPrim = gaussianSplat.GetPrim()
        self.assertTrue(gaussianSplatPrim.HasAPI(
            UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI))
        self.assertIn("ParticleFieldSphericalHarmonicsAttributeAPI",
                      gaussianSplatPrim.GetAppliedSchemas())
        self._VerifyColorSpaceNameFallback(gaussianSplatPrim)


if __name__ == "__main__":
    unittest.main()
