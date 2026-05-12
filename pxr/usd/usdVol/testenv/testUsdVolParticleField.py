#!/pxrpythonsubst
#
# Copyright 2026 Pixar
#
# Licensed under the terms set forth in the LICENSE.txt file available at
# https://openusd.org/license.

import unittest
from pxr import Usd, UsdVol


class TestUsdVolParticleField(unittest.TestCase):

    _ColorSpaceFallback = "unknown"

    def _GetCoefficientAttrs(self, prim):
        attrAPI = UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI(prim)

        self.assertFalse(callable(getattr(attrAPI, "ColorSpaceAPI", None)))
        self.assertFalse(
            callable(getattr(attrAPI, "GetColorSpaceNameAttr", None)))
        self.assertFalse(
            callable(getattr(attrAPI, "CreateColorSpaceNameAttr", None)))
        self.assertFalse(prim.HasAPI(Usd.ColorSpaceAPI))

        coefficientsAttr = (
            attrAPI.GetRadianceSphericalHarmonicsCoefficientsAttr())
        self.assertTrue(coefficientsAttr)
        coefficientshAttr = (
            attrAPI.GetRadianceSphericalHarmonicsCoefficientshAttr())
        self.assertTrue(coefficientshAttr)

        self.assertFalse(prim.GetAttribute("colorSpace:name"))
        return coefficientsAttr, coefficientshAttr

    def _VerifyNoCoefficientColorSpaceFallback(self, prim):
        coefficientsAttr, coefficientshAttr = self._GetCoefficientAttrs(prim)

        self.assertEqual(coefficientsAttr.GetColorSpace(), "")
        self.assertEqual(
            Usd.ColorSpaceAPI.ComputeColorSpaceName(coefficientsAttr), "")
        self.assertEqual(coefficientshAttr.GetColorSpace(), "")
        self.assertEqual(
            Usd.ColorSpaceAPI.ComputeColorSpaceName(coefficientshAttr), "")

    def _VerifyCoefficientColorSpaceFallback(self, prim):
        coefficientsAttr, coefficientshAttr = self._GetCoefficientAttrs(prim)

        self.assertEqual(coefficientsAttr.GetColorSpace(),
                         self._ColorSpaceFallback)
        self.assertEqual(
            Usd.ColorSpaceAPI.ComputeColorSpaceName(coefficientsAttr),
            self._ColorSpaceFallback)

        self.assertEqual(coefficientshAttr.GetColorSpace(),
                         self._ColorSpaceFallback)
        self.assertEqual(
            Usd.ColorSpaceAPI.ComputeColorSpaceName(coefficientshAttr),
            self._ColorSpaceFallback)

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
        self.assertNotIn("ColorSpaceAPI", particleFieldPrim.GetAppliedSchemas())
        self._VerifyNoCoefficientColorSpaceFallback(particleFieldPrim)

        gaussianSplat = UsdVol.ParticleField3DGaussianSplat.Define(
            stage, "/GaussianSplat")
        gaussianSplatPrim = gaussianSplat.GetPrim()
        self.assertTrue(gaussianSplatPrim.HasAPI(
            UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI))
        self.assertIn("ParticleFieldSphericalHarmonicsAttributeAPI",
                      gaussianSplatPrim.GetAppliedSchemas())
        self.assertNotIn("ColorSpaceAPI", gaussianSplatPrim.GetAppliedSchemas())
        self._VerifyCoefficientColorSpaceFallback(gaussianSplatPrim)


if __name__ == "__main__":
    unittest.main()
