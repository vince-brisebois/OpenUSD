#!/pxrpythonsubst
#
# Copyright 2026 Pixar
#
# Licensed under the terms set forth in the LICENSE.txt file available at
# https://openusd.org/license.

import unittest
from pxr import Gf, Sdf, Usd, UsdGeom, UsdVol


class TestUsdVolParticleFieldColorSpace(unittest.TestCase):
    def test_GaussianSplatDefaultsAndOverrides(self):
        stage = Usd.Stage.CreateInMemory()
        root = UsdGeom.Xform.Define(stage, '/Root').GetPrim()
        Usd.ColorSpaceAPI.Apply(root).CreateColorSpaceNameAttr('lin_ap1_scene')
        splat = UsdVol.ParticleField3DGaussianSplat.Define(stage, '/Root/Splat')
        prim = splat.GetPrim()
        Usd.ColorSpaceAPI.Apply(prim).CreateColorSpaceNameAttr('lin_rec2020_scene')

        # The typed schema specializes both representations without authoring
        # property specs or changing the raw coefficient types.
        for name, valueType in (
                ('radiance:sphericalHarmonicsCoefficients',
                 Sdf.ValueTypeNames.Float3Array),
                ('radiance:sphericalHarmonicsCoefficientsh',
                 Sdf.ValueTypeNames.Half3Array)):
            attr = prim.GetAttribute(name)
            self.assertEqual(attr.GetTypeName(), valueType)
            self.assertFalse(attr.HasAuthoredMetadata('colorSpace'))
            self.assertEqual(attr.GetColorSpace(), 'srgb_rec709_display')
            self.assertEqual(Usd.ColorSpaceAPI.ComputeColorSpaceName(attr, None),
                             'srgb_rec709_display')
            attr.SetColorSpace('lin_ap1_scene')
            self.assertEqual(Usd.ColorSpaceAPI.ComputeColorSpaceName(attr, None),
                             'lin_ap1_scene')
            attr.ClearColorSpace()
            self.assertEqual(Usd.ColorSpaceAPI.ComputeColorSpaceName(attr, None),
                             'srgb_rec709_display')

        # The default applies only to the reconstructed SH color.
        self.assertEqual(Usd.ColorSpaceAPI.ComputeColorSpaceName(
            splat.GetDisplayColorAttr(), None), 'lin_rec2020_scene')

    def test_GenericSHInheritsColorSpace(self):
        stage = Usd.Stage.CreateInMemory()
        root = UsdGeom.Xform.Define(stage, '/Root').GetPrim()
        field = UsdVol.ParticleField.Define(stage, '/Root/Field')
        sh = UsdVol.ParticleFieldSphericalHarmonicsAttributeAPI.Apply(field.GetPrim())
        for attr in (sh.GetRadianceSphericalHarmonicsCoefficientsAttr(),
                     sh.GetRadianceSphericalHarmonicsCoefficientshAttr()):
            self.assertEqual(attr.GetColorSpace(), '')
            self.assertEqual(Usd.ColorSpaceAPI.ComputeColorSpaceName(attr, None), '')
        Usd.ColorSpaceAPI.Apply(root).CreateColorSpaceNameAttr('lin_ap1_scene')
        for attr in (sh.GetRadianceSphericalHarmonicsCoefficientsAttr(),
                     sh.GetRadianceSphericalHarmonicsCoefficientshAttr()):
            self.assertEqual(Usd.ColorSpaceAPI.ComputeColorSpaceName(attr, None),
                             'lin_ap1_scene')

    def test_DisplaySRGBConversion(self):
        name = Gf.ColorSpaceNames.SRGBRec709Display
        self.assertEqual(name, 'srgb_rec709_display')
        self.assertTrue(Gf.ColorSpace.IsValid(name))
        display = Gf.ColorSpace(name)
        scene = Gf.ColorSpace(Gf.ColorSpaceNames.SRGBRec709)
        linear = Gf.ColorSpace(Gf.ColorSpaceNames.LinearRec709)
        for rgb in (Gf.Vec3f(0.02, 0.5, 0.8), Gf.Vec3f(1, 0, 0)):
            self.assertTrue(Gf.IsClose(
                Gf.Color(Gf.Color(rgb, display), linear).GetRGB(),
                Gf.Color(Gf.Color(rgb, scene), linear).GetRGB(), 1e-6))


if __name__ == '__main__':
    unittest.main()
