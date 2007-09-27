
"""
Tests for L{xmantissa.liveform}.
"""

from xml.dom.minidom import parseString

from zope.interface import implements

from twisted.trial.unittest import TestCase

from nevow.page import renderer
from nevow.tags import directive, div, span
from nevow.loaders import stan
from nevow.flat import flatten
from nevow.inevow import IQ
from nevow.athena import expose

from xmantissa.liveform import (
    FORM_INPUT, TEXT_INPUT, PASSWORD_INPUT, CHOICE_INPUT, Parameter,
    TextParameterView, PasswordParameterView, ChoiceParameter,
    ChoiceParameterView, Option, OptionView, LiveForm, ListParameter,
    ListChangeParameterView, ListChangeParameter,
    RepeatedLiveFormWrapper,_LIVEFORM_JS_CLASS, _SUBFORM_JS_CLASS, EditObject)

from xmantissa.webtheme import getLoader
from xmantissa.test.rendertools import TagTestingMixin, renderLiveFragment
from xmantissa.ixmantissa import IParameterView


class StubView(object):
    """
    Behaviorless implementation of L{IParameterView} used where such an object
    is required by tests.
    """
    implements(IParameterView)

    patternName = 'text'

    def setDefaultTemplate(self, tag):
        """
        Ignore the default template tag.
        """



class ParameterTestsMixin:
    """
    Mixin defining various tests common to different parameter view objects.
    """
    def viewFactory(self, parameter):
        """
        Instantiate a view object for the given parameter.
        """
        raise NotImplementedError("%s did not implement viewFactory")


    def test_comparison(self):
        """
        Parameter view objects should compare equal to other view objects of
        the same type which wrap the same underlying parameter object.
        """
        self.assertTrue(self.viewFactory(self.param) == self.viewFactory(self.param))
        self.assertFalse(self.viewFactory(self.param) != self.viewFactory(self.param))
        self.assertFalse(self.viewFactory(self.param) == object())
        self.assertTrue(self.viewFactory(self.param) != object())


    def test_name(self):
        """
        The I{name} renderer of the view object should render the name of the
        L{Parameter} it wraps as a child of the tag it is given.
        """
        tag = div()
        renderedName = renderer.get(self.view, 'name')(None, tag)
        self.assertTag(tag, 'div', {}, [self.name])


    def test_label(self):
        """
        The I{label} renderer of the view object should render the label of
        the L{Parameter} it wraps as a child of the tag it is given.
        """
        tag = div()
        renderedLabel = renderer.get(self.view, 'label')(None, tag)
        self.assertTag(tag, 'div', {}, [self.label])


    def test_withoutLabel(self):
        """
        The I{label} renderer of the view object should do nothing if the
        wrapped L{Parameter} has no label.
        """
        tag = div()
        self.param.label = None
        renderedOptions = renderer.get(self.view, 'label')(None, tag)
        self.assertTag(renderedOptions, 'div', {}, [])


    def _defaultRenderTest(self, fragmentName):
        loader = getLoader(fragmentName)
        document = loader.load()
        patternName = self.view.patternName + '-input-container'
        pattern = IQ(document).onePattern(patternName)
        self.view.setDefaultTemplate(pattern)
        html = flatten(self.view)

        # If it parses, well, that's the best we can do, given an arbitrary
        # template.
        document = parseString(html)


    def test_renderWithDefault(self):
        """
        The parameter view should be renderable using the default template.
        """
        return self._defaultRenderTest('liveform')


    def test_renderWithCompact(self):
        """
        The parameter view should be renderable using the compact template.
        """
        return self._defaultRenderTest('liveform-compact')



class TextLikeParameterViewTestsMixin:
    """
    Mixin defining tests for parameter views which are simple text fields.
    """
    def type():
        def get(self):
            raise AttributeError("%s did not define the type attribute")
        return get,
    type = property(*type())

    name = u'param name'
    label = u'param label'
    coercer = lambda value: value
    description = u'param desc'
    default = u'param default value'


    def setUp(self):
        """
        Create a L{Parameter} and a L{TextParameterView} wrapped around it.
        """
        self.param = Parameter(
            self.name, self.type, self.coercer, self.label, self.description,
            self.default)
        self.view = self.viewFactory(self.param)


    def test_default(self):
        """
        L{TextParameterView.value} should render the default value of the
        L{Parameter} it wraps as a child of the tag it is given.
        """
        tag = div()
        renderedDefault = renderer.get(self.view, 'default')(None, tag)
        self.assertTag(tag, 'div', {}, [self.default])


    def test_withoutDefault(self):
        """
        L{TextParameterView.value} should leave the tag it is given unchanged
        if the L{Parameter} it wraps has a C{None} default.
        """
        tag = div()
        self.param.default = None
        renderedDefault = renderer.get(self.view, 'default')(None, tag)
        self.assertTag(tag, 'div', {}, [])


    def test_description(self):
        """
        L{TextParameterView.description} should render the description of the
        L{Parameter} it wraps as a child of the tag it is given.
        """
        tag = div()
        renderedDescription = renderer.get(self.view, 'description')(None, tag)
        self.assertTag(tag, 'div', {}, [self.description])


    def test_withoutDescription(self):
        """
        L{TextParameterView.description} should leave the tag it is given
        unchanged if the L{Parameter} it wraps has no description.
        """
        tag = div()
        self.param.description = None
        renderedDescription = renderer.get(self.view, 'description')(None, tag)
        self.assertTag(tag, 'div', {}, [])


    def test_renderCompletely(self):
        """
        L{TextParameterView} should be renderable in the usual Nevow manner.
        """
        self.view.docFactory = stan(div[
                div(render=directive('name')),
                div(render=directive('label')),
                div(render=directive('default')),
                div(render=directive('description'))])
        html = flatten(self.view)
        self.assertEqual(
            html,
            '<div><div>param name</div><div>param label</div>'
            '<div>param default value</div><div>param desc</div></div>')



class TextParameterViewTests(TextLikeParameterViewTestsMixin,
                             TestCase, ParameterTestsMixin,
                             TagTestingMixin):
    """
    Tests for the view generation code for C{TEXT_INPUT} L{Parameter}
    instances.
    """
    type = TEXT_INPUT
    viewFactory = TextParameterView



class PasswordParameterViewTests(TextLikeParameterViewTestsMixin,
                                 TestCase, ParameterTestsMixin,
                                 TagTestingMixin):
    """
    Tests for the view generation code for C{PASSWORD_INPUT} L{Parameter}
    instances.
    """
    type = PASSWORD_INPUT
    viewFactory = PasswordParameterView



class ChoiceParameterTests(TestCase, ParameterTestsMixin, TagTestingMixin):
    """
    Tests for the view generation code for C{CHOICE_INPUT} L{Parameter}
    instances.
    """
    viewFactory = ChoiceParameterView

    def setUp(self):
        """
        Create a L{Parameter} and a L{ChoiceParameterView} wrapped around it.
        """
        self.type = CHOICE_INPUT
        self.name = u'choice name'
        self.choices = [
            Option(u'description one', u'value one', False),
            Option(u'description two', u'value two', False)]
        self.label = u'choice label'
        self.description = u'choice description'
        self.multiple = False
        self.param = ChoiceParameter(
            self.name, self.choices, self.label, self.description,
            self.multiple)
        self.view = self.viewFactory(self.param)


    def test_multiple(self):
        """
        L{ChoiceParameterView.multiple} should render the multiple attribute on
        the tag it is passed if the wrapped L{ChoiceParameter} is a
        L{MULTI_CHOICE_INPUT}.
        """
        tag = div()
        self.param.multiple = True
        renderedSelect = renderer.get(self.view, 'multiple')(None, tag)
        self.assertTag(tag, 'div', {'multiple': 'multiple'}, [])


    def test_single(self):
        """
        L{ChoiceParameterView.multiple} should not render the multiple
        attribute on the tag it is passed if the wrapped L{ChoiceParameter} is
        a L{CHOICE_INPUT}.
        """
        tag = div()
        renderedSelect = renderer.get(self.view, 'multiple')(None, tag)
        self.assertTag(tag, 'div', {}, [])


    def test_options(self):
        """
        L{ChoiceParameterView.options} should load the I{option} pattern from
        the tag it is passed and add copies of it as children to the tag for
        all of the options passed to L{ChoiceParameterView.__init__}.
        """
        option = span(pattern='option')
        tag = div[option]
        renderedOptions = renderer.get(self.view, 'options')(None, tag)
        self.assertEqual(
            renderedOptions.children[1:],
            [OptionView(index, c, None)
             for (index, c)
             in enumerate(self.choices)])


    def test_description(self):
        """
        L{ChoiceParameterView.description} should add the description of the
        wrapped L{ChoiceParameter} to the tag it is passed.
        """
        tag = div()
        renderedOptions = renderer.get(self.view, 'description')(None, tag)
        self.assertTag(renderedOptions, 'div', {}, [self.description])


    def test_withoutDescription(self):
        """
        L{ChoiceParameterView.description} should do nothing if the wrapped
        L{ChoiceParameter} has no description.
        """
        tag = div()
        self.param.description = None
        renderedOptions = renderer.get(self.view, 'description')(None, tag)
        self.assertTag(renderedOptions, 'div', {}, [])



class OptionTests(TestCase, TagTestingMixin):
    """
    Tests for the view generation code for a single choice, L{OptionView}.
    """
    simpleOptionTag = stan(div[
            div(render=directive('description')),
            div(render=directive('value')),
            div(render=directive('index')),
            div(render=directive('selected'))])

    def setUp(self):
        """
        Create an L{Option} and an L{OptionView} wrapped around it.
        """
        self.description = u'option description'
        self.value = u'option value'
        self.selected = True
        self.option = Option(self.description, self.value, self.selected)
        self.index = 3
        self.view = OptionView(self.index, self.option, self.simpleOptionTag)


    def test_description(self):
        """
        L{OptionView.description} should add the description of the option it
        wraps as a child to the tag it is passed.
        """
        tag = div()
        renderedDescription = renderer.get(self.view, 'description')(None, tag)
        self.assertTag(renderedDescription, 'div', {}, [self.description])


    def test_value(self):
        """
        L{OptionView.value} should add the value of the option it wraps as a
        child to the tag it is passed.
        """
        tag = div()
        renderedValue = renderer.get(self.view, 'value')(None, tag)
        self.assertTag(renderedValue, 'div', {}, [self.value])


    def test_index(self):
        """
        L{OptionView.index} should add the index passed to
        L{OptionView.__init__} to the tag it is passed.
        """
        tag = div()
        renderedIndex = renderer.get(self.view, 'index')(None, tag)
        self.assertTag(renderedIndex, 'div', {}, [self.index])


    def test_selected(self):
        """
        L{OptionView.selected} should add a I{selected} attribute to the tag it
        is passed if the option it wraps is selected.
        """
        tag = div()
        renderedValue = renderer.get(self.view, 'selected')(None, tag)
        self.assertTag(renderedValue, 'div', {'selected': 'selected'}, [])


    def test_notSelected(self):
        """
        L{OptionView.selected} should not add a I{selected} attribute to the
        tag it is passed if the option it wraps is not selected.
        """
        self.option.selected = False
        tag = div()
        renderedValue = renderer.get(self.view, 'selected')(None, tag)
        self.assertTag(renderedValue, 'div', {}, [])


    def test_renderCompletely(self):
        """
        L{ChoiceParameterView} should be renderable in the usual Nevow manner.
        """
        html = flatten(self.view)
        self.assertEqual(
            html,
            '<div><div>option description</div><div>option value</div>'
            '<div>3</div><div selected="selected"></div></div>')



class LiveFormTests(TestCase, TagTestingMixin):
    """
    Tests for the form generation code in L{LiveForm}.
    """
    # Minimal tag which can be used with the form renderer.  Classes are only
    # used to tell nodes apart in the tests.
    simpleLiveFormTag = div[
        span(pattern='text-input-container'),
        span(pattern='password-input-container'),
        span(pattern='liveform', _class='liveform-container'),
        span(pattern='subform', _class='subform-container')]


    def test_compact(self):
        """
        L{LiveForm.compact} should replace the existing C{docFactory} with one
        for the I{compact} version of the live form template.
        """
        form = LiveForm(None, [])
        form.compact()
        self.assertTrue(form.docFactory.template.endswith('/liveform-compact.html'))


    def test_recursiveCompact(self):
        """
        L{LiveForm.compact} should also call C{compact} on all of its subforms.
        """
        class StubChild(object):
            compacted = False
            def compact(self):
                self.compacted = True
        child = StubChild()
        form = LiveForm(None, [Parameter('foo', FORM_INPUT, child),
                               Parameter('bar', TEXT_INPUT, int),
                               ListParameter('baz', None, 3),
                               ChoiceParameter('quux', [])])
        form.compact()
        self.assertTrue(child.compacted)


    def test_descriptionSlot(self):
        """
        L{LiveForm.form} should fill the I{description} slot on the tag it is
        passed with the description of the form.
        """
        description = u"the form description"
        formFragment = LiveForm(None, [], description)
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertEqual(formTag.slotData['description'], description)


    def test_formSlotOuter(self):
        """
        When it is not nested inside another form, L{LiveForm.form} should fill
        the I{form} slot on the tag with the tag's I{liveform} pattern.
        """
        def submit(**kw):
            pass
        formFragment = LiveForm(submit, [])
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertTag(
            formTag.slotData['form'], 'span', {'class': 'liveform-container'},
            [])


    def test_formSlotInner(self):
        """
        When it has a sub-form name, L{LiveForm.form} should fill the I{form}
        slot on the tag with the tag's I{subform} pattern.
        """
        def submit(**kw):
            pass
        formFragment = LiveForm(submit, [])
        formFragment.subFormName = 'test-subform'
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertTag(
            formTag.slotData['form'], 'span', {'class': 'subform-container'},
            [])


    def test_noParameters(self):
        """
        When there are no parameters, L{LiveForm.form} should fill the
        I{inputs} slot on the tag it uses to fill the I{form} slot with an
        empty list.
        """
        def submit(**kw):
            pass
        formFragment = LiveForm(submit, [])
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertEqual(formTag.slotData['form'].slotData['inputs'], [])


    def test_parameterViewOverride(self):
        """
        L{LiveForm.form} should use the C{view} attribute of parameter objects,
        if it is not C{None}, to fill the I{inputs} slot on the tag it uses to
        fill the I{form} slot.
        """
        def submit(**kw):
            pass

        name = u'param name'
        label = u'param label'
        type = TEXT_INPUT
        coercer = lambda value: value
        description = u'param desc'
        default = u'param default value'

        view = StubView()
        views = {}
        viewFactory = views.get
        param = Parameter(
            name, type, coercer, label, description, default, viewFactory)
        views[param] = view

        formFragment = LiveForm(submit, [param])
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertEqual(
            formTag.slotData['form'].slotData['inputs'],
            [view])


    def test_individualTextParameter(self):
        """
        L{LiveForm.form} should fill the I{inputs} slot on the tag it uses to
        fill the I{form} slot with a list consisting of one
        L{TextParameterView} when the L{LiveForm} is created with one
        C{TEXT_INPUT} L{Parameter}.
        """
        def submit(**kw):
            pass

        name = u'param name'
        label = u'param label'
        type = TEXT_INPUT
        coercer = lambda value: value
        description = u'param desc'
        default = u'param default value'
        param = Parameter(
            name, type, coercer, label, description, default)

        formFragment = LiveForm(submit, [param])
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertEqual(
            formTag.slotData['form'].slotData['inputs'],
            [TextParameterView(param)])


    def test_individualPasswordParameter(self):
        """
        L{LiveForm.form} should fill the I{inputs} slot of the tag it uses to
        fill the I{form} slot with a list consisting of one
        L{TextParameterView} when the L{LiveForm} is created with one
        C{PASSWORD_INPUT} L{Parameter}.
        """
        def submit(**kw):
            pass

        name = u'param name'
        label = u'param label'
        type = PASSWORD_INPUT
        coercer = lambda value: value
        description = u'param desc'
        default = u'param default value'
        param = Parameter(
            name, type, coercer, label, description, default)

        formFragment = LiveForm(submit, [param])
        formTag = formFragment.form(None, self.simpleLiveFormTag)
        self.assertEqual(
            formTag.slotData['form'].slotData['inputs'],
            [PasswordParameterView(param)])


    def test_liveformTemplateStructuredCorrectly(self):
        """
        When a L{LiveForm} is rendered using the default template, the form
        contents should end up inside the I{form} tag.

        As I understand it, this is a necessary condition for the resulting
        html form to operate properly.  However, due to the complex behavior of
        the HTML (or even XHTML) DOM and the inscrutability of the various
        specific implementations of it, it is not entirely unlikely that my
        understanding is, in some way, flawed.  If you know better, and believe
        this test to be in error, supplying a superior test or simply deleting
        this one may not be out of the question. -exarkun
        """
        def submit(**kw):
            pass

        name = u'param name'
        label = u'param label'
        type = PASSWORD_INPUT
        coercer = lambda value: value
        description = u'param desc'
        default = u'param default value'
        param = Parameter(
            name, type, coercer, label, description, default)

        formFragment = LiveForm(submit, [param])
        html = renderLiveFragment(formFragment)
        document = parseString(html)
        forms = document.getElementsByTagName('form')
        self.assertEqual(len(forms), 1)
        inputs = forms[0].getElementsByTagName('input')
        self.assertTrue(len(inputs) >= 1)


    def test_liveFormJSClass(self):
        """
        Verify that the C{jsClass} attribute of L{LiveForm} is
        L{_LIVEFORM_JS_CLASS}.
        """
        self.assertEqual(LiveForm.jsClass, _LIVEFORM_JS_CLASS)


    def test_subFormJSClass(self):
        """
        Verify that the C{jsClass} attribute of the form returned from
        L{LiveForm.asSubForm} is L{_SUBFORM_JS_CLASS}.
        """
        liveForm = LiveForm(lambda **k: None, ())
        subForm = liveForm.asSubForm(u'subform')
        self.assertEqual(subForm.jsClass, _SUBFORM_JS_CLASS)



class ListChangeParameterViewTestCase(TestCase):
    """
    Tests for L{ListChangeParameterView}.
    """
    def setUp(self):
        class TestableLiveForm(LiveForm):
            _isCompact = False
            def compact(self):
                self._isCompact = True
        self.innerParameters = [Parameter('foo', TEXT_INPUT, int)]
        self.parameter = ListChangeParameter(
            u'repeatableFoo', self.innerParameters, defaults=[], modelObjects=[])
        self.parameter.liveFormFactory = TestableLiveForm
        self.parameter.repeatedLiveFormWrapper = RepeatedLiveFormWrapper
        self.view = ListChangeParameterView(self.parameter)


    def test_patternName(self):
        """
        L{ListChangeParameterView} should use I{repeatable-form} as its
        C{patternName}
        """
        self.assertEqual(self.view.patternName, 'repeatable-form')


    def _doSubFormTest(self, subFormWrapper):
        """
        C{subFormWrapper} (which we expect to be the result of
        L{self.parameter.formFactory}, wrapped in
        L{self.parameter.repeatedLiveFormWrapper) should be a render-ready
        liveform that knows its a subform.
        """
        self.failUnless(
            isinstance(subFormWrapper, RepeatedLiveFormWrapper))
        self.assertIdentical(subFormWrapper.fragmentParent, self.view)
        subForm = subFormWrapper.liveForm
        self.assertEqual(self.innerParameters, subForm.parameters)
        self.assertEqual(subForm.subFormName, 'subform')


    def test_formsRendererReturnsSubForm(self):
        """
        The C{forms} renderer of L{ListChangeParameterView} should render
        the liveform that was passed to the underlying parameter, as a
        subform.
        """
        (form,) = renderer.get(self.view, 'forms')(None, None)
        self._doSubFormTest(form)


    def test_repeatFormReturnsSubForm(self):
        """
        The C{repeatForm} exposed method of L{ListChangeParameterView}
        should return the liveform that was passed to the underlying
        parameter, as a subform.
        """
        self._doSubFormTest(expose.get(self.view, 'repeatForm')())


    def test_formsRendererCompact(self):
        """
        The C{forms} renderer of L{ListChangeParameterView} should call
        C{compact} on the form it returns, if the parameter it is wrapping had
        C{compact} called on it.
        """
        self.parameter.compact()
        (renderedForm,) = renderer.get(self.view, 'forms')(None, None)
        self.failUnless(renderedForm.liveForm._isCompact)


    def test_repeatFormCompact(self):
        """
        The C{repeatForm} exposed method of of L{ListChangeParameterView}
        should call C{compact} on the form it returns, if the parameter it is
        wrapping had C{compact} called on it.
        """
        self.parameter.compact()
        renderedForm = expose.get(self.view, 'repeatForm')()
        self.failUnless(renderedForm.liveForm._isCompact)


    def test_formsRendererNotCompact(self):
        """
        The C{forms} renderer of L{ListChangeParameterView} shouldn't call
        C{compact} on the form it returns, unless the parameter it is wrapping
        had C{compact} called on it.
        """
        (renderedForm,) = renderer.get(self.view, 'forms')(None, None)
        self.failIf(renderedForm.liveForm._isCompact)


    def test_repeatFormNotCompact(self):
        """
        The C{repeatForm} exposed method of L{ListChangeParameterView}
        shouldn't call C{compact} on the form it returns, unless the parameter
        it is wrapping had C{compact} called on it.
        """
        renderedForm = expose.get(self.view, 'repeatForm')()
        self.failIf(renderedForm.liveForm._isCompact)


    def test_repeaterRenderer(self):
        """
        The C{repeater} renderer of L{ListChangeParameterView} should
        return an instance of the C{repeater} pattern from its docFactory.
        """
        self.view.docFactory = stan(div(pattern='repeater', foo='bar'))
        renderedTag = renderer.get(self.view, 'repeater')(None, None)
        self.assertEqual(renderedTag.attributes['foo'], 'bar')



class ListChangeParameterTestCase(TestCase):
    """
    Tests for L{ListChangeParameter}.
    """
    _someParameters = (Parameter('foo', TEXT_INPUT, int),)

    def setUp(self):
        self.innerParameters = [Parameter('foo', TEXT_INPUT, int)]
        self.defaultValues = {u'foo': -56}
        self.defaultObject = object()

        self.parameter = ListChangeParameter(
            u'repeatableFoo', self.innerParameters,
            defaults=[self.defaultValues],
            modelObjects=[self.defaultObject])


    def getListChangeParameter(self, parameters, defaults):
        return ListChangeParameter(
            name=u'stateRepeatableFoo', parameters=parameters,
            defaults=defaults,
            modelObjects=[object() for i in range(len(defaults))])


    def test_asLiveForm(self):
        """
        L{ListChangeParameter.asLiveForm} should wrap forms in
        L{ListChangeParameter.liveFormWrapperFactory}.
        """
        parameter = self.getListChangeParameter(self._someParameters, [])
        parameter.repeatedLiveFormWrapper = RepeatedLiveFormWrapper

        liveFormWrapper = parameter.asLiveForm()
        self.failUnless(
            isinstance(liveFormWrapper, RepeatedLiveFormWrapper))
        liveForm = liveFormWrapper.liveForm
        self.failUnless(isinstance(liveForm, LiveForm))
        self.assertEqual(liveForm.subFormName, 'subform')
        self.assertEqual(liveForm.parameters, self._someParameters)


    def test_getInitialLiveForms(self):
        """
        Same as L{test_asLiveForm}, but looks at the single liveform returned
        from L{ListChangeParameter.getInitialLiveForms} when the parameter
        was constructed with no defaults.
        """
        parameter = self.getListChangeParameter(self._someParameters, [])
        parameter.repeatedLiveFormWrapper = RepeatedLiveFormWrapper

        liveFormWrappers = parameter.getInitialLiveForms()
        self.assertEqual(len(liveFormWrappers), 1)

        liveFormWrapper = liveFormWrappers[0]
        self.failUnless(
            isinstance(liveFormWrapper, RepeatedLiveFormWrapper))
        liveForm = liveFormWrapper.liveForm
        self.failUnless(isinstance(liveForm, LiveForm))
        self.assertEqual(liveForm.subFormName, 'subform')
        self.assertEqual(liveForm.parameters, self._someParameters)


    def test_getInitialLiveFormsDefaults(self):
        """
        Same as L{test_getInitialLiveForms}, but for the case where the
        parameter was constructed with default values.
        """
        defaults = [{'foo': 1}, {'foo': 3}]
        parameter = self.getListChangeParameter(self._someParameters, defaults)
        parameter.repeatedLiveFormWrapper = RepeatedLiveFormWrapper

        liveFormWrappers = parameter.getInitialLiveForms()
        self.assertEqual(len(liveFormWrappers), len(defaults))
        for (liveFormWrapper, default) in zip(liveFormWrappers, defaults):
            self.failUnless(
                isinstance(liveFormWrapper, RepeatedLiveFormWrapper))

            liveForm = liveFormWrapper.liveForm
            self.failUnless(isinstance(liveForm, LiveForm))
            self.assertEqual(liveForm.subFormName, 'subform')
            self.assertEqual(len(liveForm.parameters), 1)

            # Matches up with self._someParameters, except the default should
            # be different.
            parameter = liveForm.parameters[0]
            self.assertEqual(parameter.name, 'foo')
            self.assertEqual(parameter.type, TEXT_INPUT)
            self.assertEqual(parameter.coercer, int)
            self.assertEqual(parameter.default, default['foo'])


    def test_identifierMapping(self):
        """
        L{ListChangeParameter} should be able to freely convert between
        python objects and the opaque identifiers generated from them.
        """
        defaultObject = object()
        identifier = self.parameter._idForObject(defaultObject)
        self.assertIdentical(
            self.parameter._objectFromID(identifier), defaultObject)


    def test_coercion(self):
        """
        L{ListChangeParameter._coerceSingleRepetition} should call the
        appropriate coercers from the repeatable form's parameters.
        """
        self.assertEqual(
            self.parameter._coerceSingleRepetition({u'foo': [u'-56']}), {u'foo': -56})


    def test_coercerCreate(self):
        """
        L{ListChangeParameter.coercer} should be able to figure out that a
        repetition is new if it is associated with an identifier generated by
        C{asLiveForm}.
        """
        parameter = ListChangeParameter(
            u'repeatableFoo', self.innerParameters,
            defaults=[],
            modelObjects=[])

        # get an id allocated to us
        liveFormWrapper = parameter.asLiveForm()
        submission = parameter.coercer(
            [{u'foo': [u'-56'],
              parameter._IDENTIFIER_KEY: liveFormWrapper.identifier}])
        self.assertEqual(submission.edit, [])
        self.assertEqual(submission.delete, [])
        self.assertEqual(len(submission.create), 1)
        self.assertEqual(submission.create[0].values, {u'foo': -56})
        CREATED_OBJECT = object()
        submission.create[0].setter(CREATED_OBJECT)
        self.assertIdentical(
            parameter._objectFromID(liveFormWrapper.identifier),
            CREATED_OBJECT)


    def test_coercerCreateNoChange(self):
        """
        L{ListChangeParameter.coercer} should be able to figure out when
        nothing has been done to a set of values created by a previous
        submission.
        """
        parameter = ListChangeParameter(
            u'repeatableFoo', self.innerParameters,
            defaults=[],
            modelObjects=[])

        # get an id allocated to us
        liveFormWrapper = parameter.asLiveForm()
        identifier = liveFormWrapper.identifier

        value = {u'foo': [u'-56'], parameter._IDENTIFIER_KEY: identifier}
        firstSubmission = parameter.coercer([value.copy()])
        firstSubmission.create[0].setter(None)
        secondSubmission = parameter.coercer([value.copy()])
        self.assertEqual(secondSubmission.create, [])
        self.assertEqual(secondSubmission.edit, [])
        self.assertEqual(secondSubmission.delete, [])


    def test_coercerEdit(self):
        """
        L{ListChangeParameter.coercer} should be able to figure out that a
        repetition is an edit if its identifier corresponds to an entry in the
        list of defaults.
        """
        (identifier,) = self.parameter._idsToObjects.keys()

        submission = self.parameter.coercer(
            [{u'foo': [u'-57'],
              self.parameter._IDENTIFIER_KEY: identifier}])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit,
                         [EditObject(self.defaultObject, {u'foo': -57})])
        self.assertEqual(submission.delete, [])


    def test_repeatedCoercerEdit(self):
        """
        L{ListChangeParameter.coercer} should work correctly with respect
        to repeated edits.
        """
        (identifier,) = self.parameter._idsToObjects.keys()

        self.parameter.coercer(
            [{u'foo': [u'-57'], self.parameter._IDENTIFIER_KEY: identifier}])
        # edit it back to the initial value
        submission = self.parameter.coercer(
            [{u'foo': [u'-56'], self.parameter._IDENTIFIER_KEY: identifier}])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit,
                         [EditObject(self.defaultObject, {u'foo': -56})])
        self.assertEqual(submission.delete, [])


    def test_coercerNoChange(self):
        """
        L{ListChangeParameter.coercer} shouldn't include a repetition
        anywhere in its result if it corresponds to a default and wasn't
        edited.
        """
        (identifier,) = self.parameter._idsToObjects.keys()

        submission = self.parameter.coercer(
            [{u'foo': [u'-56'],
              self.parameter._IDENTIFIER_KEY: identifier}])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit, [])
        self.assertEqual(submission.delete, [])


    def test_repeatedCoercerNoChange(self):
        """
        Same as L{test_coercerNoChange}, but with multiple submissions that
        don't change anything.
        """
        (identifier,) = self.parameter._idsToObjects.keys()

        self.parameter.coercer(
            [{u'foo': [u'-56'],
              self.parameter._IDENTIFIER_KEY: identifier}])

        submission = self.parameter.coercer(
            [{u'foo': [u'-56'],
              self.parameter._IDENTIFIER_KEY: identifier}])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit, [])
        self.assertEqual(submission.delete, [])


    def test_coercerDelete(self):
        """
        L{ListChangeParameter.coercer} should be able to figure out that a
        default was deleted if it doesn't get a repetition with a
        corresponding identifier.
        """
        submission = self.parameter.coercer([])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit, [])
        self.assertEqual(submission.delete, [self.defaultObject])


    def test_repeatedCoercerDelete(self):
        """
        L{ListChangeParameter.coercer} should only report a deletion the
        first time that it doesn't see a particular value.
        """
        self.parameter.coercer([])
        submission = self.parameter.coercer([])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit, [])
        self.assertEqual(submission.delete, [])


    def test_coercerDeleteUnsubmitted(self):
        """
        L{ListChangeParameter.coercer} should not report as deleted an
        internal marker objects when a form is repeated but the repetition is
        omitted from the submission.
        """
        (identifier,) = self.parameter._idsToObjects.keys()
        repetition = self.parameter.asLiveForm()
        submission = self.parameter.coercer([
            {u'foo': [u'-56'],
             self.parameter._IDENTIFIER_KEY: identifier}])
        self.assertEqual(submission.create, [])
        self.assertEqual(submission.edit, [])
        self.assertEqual(submission.delete, [])


    def test_makeDefaultLiveForm(self):
        """
        L{ListChangeParameter._makeDefaultLiveForm} should make a live
        form that has been correctly wrapped and initialized.
        """
        liveFormWrapper = self.parameter._makeDefaultLiveForm(
            (self.parameter.defaults[0], 1234))
        self.failUnless(isinstance(liveFormWrapper, self.parameter.repeatedLiveFormWrapper))
        liveForm = liveFormWrapper.liveForm
        self.failUnless(isinstance(liveForm, LiveForm))
        self.assertEqual(
            len(liveForm.parameters), len(self.innerParameters))
        for parameter in liveForm.parameters:
            self.assertEqual(parameter.default, self.defaultValues[parameter.name])


    def test_asLiveFormIdentifier(self):
        """
        L{ListChangeParameter.asLiveForm} should allocate an identifier
        for the new liveform, pass it to the liveform wrapper and put the
        placeholder value L{ListChangeParameter._NO_OBJECT_MARKER} into
        the object mapping.
        """
        liveFormWrapper = self.parameter.asLiveForm()
        self.assertIn(liveFormWrapper.identifier, self.parameter._idsToObjects)
        self.assertIdentical(
            self.parameter._objectFromID(liveFormWrapper.identifier),
            self.parameter._NO_OBJECT_MARKER)


    def test_correctIdentifiersFromGetInitialLiveForms(self):
        """
        L{ListChangeParameter.getInitialLiveForms} should return a list of
        L{RepeatedLiveFormWrapper} instances with C{identifier} attributes
        which correspond to the identifiers associated with corresponding
        model objects in the L{ListChangeParameter}.
        """
        # XXX This should really have more than one model object to make sure
        # ordering is tested properly.
        forms = self.parameter.getInitialLiveForms()
        self.assertEqual(len(forms), 1)
        self.assertIdentical(
            self.parameter._objectFromID(forms[0].identifier),
            self.defaultObject)
