import panel as pn
from panel.chat import ChatInterface, ChatMessage

from UtilityFunctions import create_chat_message, get_class_cards_from_json
from domainmodeler import DomainModeler


def remove_waiting(message):
    domChat.remove(message)
    pass


def show_waiting():
    indeterminate = pn.indicators.Progress(name='Indeterminate Progress', active=True, width=200)
    gif_pane = pn.pane.GIF('message_loading.gif', height=100, width=100)
    # indeterminate = pn.indicators.LoadingSpinner(value=True, size=20, name='Loading...')

    row = pn.Row(gif_pane, styles={'background': 'WhiteSmoke'})
    message = ChatMessage(row, user="Assistant", avatar=ChatMessage.default_avatars["tool"])
    domChat.send(message)
    return message


def show_non_role_class_structure(domain_modeler=None):
    message = create_chat_message(
        f"Find classes other than the following: {', '.join(domain_modeler.role_class_list)}.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)

    domain_modeler.get_non_role_classes()

    msg_body = get_class_cards_from_json("non_role_classes.json")
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def show_role_class_structure(role_list_to_convert, domain_modeler=None):
    message = create_chat_message(
        f"Convert the {'role' if len(role_list_to_convert) == 1 else 'roles'} {', '.join(role_list_to_convert)} into {'a class' if len(role_list_to_convert) == 1 else 'classes'}.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)

    domain_modeler.get_role_classes(role_list_to_convert)

    msg_body = get_class_cards_from_json("role_classes.json")
    non_role_class_button = pn.widgets.Button(name="Find", button_type='primary')
    pn.bind(lambda func: show_non_role_class_structure(domain_modeler), non_role_class_button,
            watch=True)
    msg_body.append(pn.Row("Do you wish to find classes other than the roles?", non_role_class_button))
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def finalize_domain_model(domain_modeler):
    message = create_chat_message("I don't wish to make any modifications. Show me the final domain model.",
                                  user="User", avatar=ChatMessage.default_avatars["human"]
                                  )
    domChat.send(message, respond=False)

    card_classes = pn.Card(title="Classes", collapsed=True, styles={'background': 'WhiteSmoke'})
    card_relationships = pn.Card(title="Relationships", collapsed=True, styles={'background': 'WhiteSmoke'})

    for cls in domain_modeler.class_list:
        card_classes.append(cls)
    for rel in domain_modeler.relationships_list:
        card_relationships.append(rel)

    file_name = domain_modeler.create_domain_model_graph()
    dom_model_graph = pn.pane.PNG(file_name + '.png')
    column = pn.Column(" ********* DOMAIN MODEL ********* ", card_classes, card_relationships)

    msg_body = column

    # msg_body = get_class_cards_from_json("role_classes.json")
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)

    msg_body = dom_model_graph
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def modify_domain_model(domain_modeler):
    pass


def put_relationship_in_domain_model(domain_modeler, relationships_to_put):
    message = create_chat_message(
        f"Put the {'relationship' if len(relationships_to_put) == 1 else 'relationships'} {','.join(str(rel) for rel in relationships_to_put)} in the domain model.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)
    domain_modeler.role_class_count = 0
    domain_modeler.role_class_list = []

    for relationship in relationships_to_put:
        domain_modeler.relationships_list.append(relationship)
        domain_modeler.relationships_count = domain_modeler.relationships_count + 1

    column = pn.Column(styles={'background': 'WhiteSmoke'})
    column.append("Relationships in the domain model: ")
    relationship_string = ""
    for rel in domain_modeler.relationships_list:
        relationship_string = relationship_string + str(rel) + "\n"

    column.append(relationship_string)
    msg_body = column

    # msg_body = get_class_cards_from_json("role_classes.json")
    finalize_domain_model_button = pn.widgets.Button(name="No ! I am done.", button_type='primary')
    pn.bind(lambda func: finalize_domain_model(domain_modeler), finalize_domain_model_button,
            watch=True)

    modify_domain_model_button = pn.widgets.Button(name="Modify", button_type='primary')
    pn.bind(lambda func: modify_domain_model(domain_modeler), modify_domain_model_button,
            watch=True)

    msg_body.append(pn.Row("Do you wish to modify domain model we created?", modify_domain_model_button,
                           finalize_domain_model_button))
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def show_relationships(domain_modeler):
    message = create_chat_message(
        f"Find relationships involved in the user stories.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)

    msg = show_waiting()

    relationships_json = domain_modeler.get_relationships_json()
    relationships_count, relationships_list = domain_modeler.read_relationships_json(relationships_json)

    remove_waiting(msg)

    relationships_checkbox_group = pn.widgets.CheckBoxGroup(name='roles', value=relationships_list,
                                                            options=relationships_list,
                                                            inline=False,
                                                            styles={'background': 'WhiteSmoke'})
    msg_body = pn.Column(f"Number of Relationships ): {relationships_count}",
                         f"Relationships:",
                         relationships_checkbox_group)

    # msg_body = get_class_cards_from_json("role_classes.json")
    put_relationships_button = pn.widgets.Button(name="Put", button_type='primary')
    pn.bind(lambda func: put_relationship_in_domain_model(domain_modeler, relationships_checkbox_group.value),
            put_relationships_button,
            watch=True)
    msg_body.append(
        pn.Row("Do you wish to put the selected relationships in the domain model?", put_relationships_button))
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def show_non_role_classes(domain_modeler):
    message = create_chat_message(
        f"Find classes other than the following: {', '.join(domain_modeler.role_class_list)}.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)

    msg = show_waiting()

    non_role_classes_json = domain_modeler.get_non_role_classes_json()
    non_role_classes_count, non_role_classes_list = domain_modeler.read_classes_json(non_role_classes_json)

    remove_waiting(msg)

    non_role_classes_checkbox_group = pn.widgets.CheckBoxGroup(name='roles', value=non_role_classes_list,
                                                               options=non_role_classes_list,
                                                               inline=False,
                                                               styles={'background': 'WhiteSmoke'})
    msg_body = pn.Column(f"Number of classes (other than roles) ): {non_role_classes_count}",
                         f"Classes:",
                         non_role_classes_checkbox_group)

    # msg_body = get_class_cards_from_json("role_classes.json")
    put_class_button = pn.widgets.Button(name="Put", button_type='primary')
    pn.bind(lambda func: put_class_in_domain_model(domain_modeler, non_role_classes_checkbox_group.value,
                                                   class_type="NON-ROLE"),
            put_class_button,
            watch=True)
    msg_body.append(pn.Row("Do you wish to put the selected classes in the domain model?", put_class_button))
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def put_class_in_domain_model(domain_modeler, classes_to_put, class_type="ROLE"):
    message = create_chat_message(
        f"Put the {'class' if len(classes_to_put) == 1 else 'classes'} {', '.join(classes_to_put)} in the domain model.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)
    if class_type == "ROLE":
        domain_modeler.role_class_count = 0
        domain_modeler.role_class_list = []

        for cls in classes_to_put:
            domain_modeler.role_class_list.append(cls)
            domain_modeler.class_list.append(cls)
            domain_modeler.role_class_count = domain_modeler.role_class_count + 1

        msg_body = pn.Column(f"Classes in the domain model: {list(set(domain_modeler.class_list))}",
                             styles={'background': 'WhiteSmoke'})

        # msg_body = get_class_cards_from_json("role_classes.json")
        non_role_classes_button = pn.widgets.Button(name="Find", button_type='primary')
        pn.bind(lambda func: show_non_role_classes(domain_modeler), non_role_classes_button,
                watch=True)
        msg_body.append(pn.Row("Do you wish to find classes other than roles?", non_role_classes_button))
        message = create_chat_message(msg_body)
        domChat.send(message, respond=False)
    elif class_type == "NON-ROLE":
        domain_modeler.non_role_class_count = 0
        domain_modeler.non_role_class_list = []

        for cls in classes_to_put:
            domain_modeler.non_role_class_list.append(cls)
            domain_modeler.class_list.append(cls)
            domain_modeler.non_role_class_count = domain_modeler.role_class_count + 1

        msg_body = pn.Column(f"Classes in the domain model: {list(set(domain_modeler.class_list))}",
                             styles={'background': 'WhiteSmoke'})

        # msg_body = get_class_cards_from_json("role_classes.json")
        relationship_button = pn.widgets.Button(name="Find", button_type='primary')
        pn.bind(lambda func: show_relationships(domain_modeler), relationship_button,
                watch=True)
        msg_body.append(pn.Row("Do you wish to find relationships between the classes?", relationship_button))
        message = create_chat_message(msg_body)
        domChat.send(message, respond=False)


def show_role_classes(role_list_to_convert, domain_modeler=None):
    message = create_chat_message(
        f"Convert the {'role' if len(role_list_to_convert) == 1 else 'roles'} {', '.join(role_list_to_convert)} into {'a class' if len(role_list_to_convert) == 1 else 'classes'}.",
        user="User", avatar=ChatMessage.default_avatars["human"]
    )
    domChat.send(message, respond=False)

    msg = show_waiting()

    role_classes_json = domain_modeler.get_role_classes_json(role_list_to_convert)
    role_classes_count, role_classes_list = domain_modeler.read_classes_json(role_classes_json)

    remove_waiting(msg)

    role_classes_checkbox_group = pn.widgets.CheckBoxGroup(name='roles', value=role_classes_list,
                                                           options=role_classes_list,
                                                           inline=False,
                                                           styles={'background': 'WhiteSmoke'})
    msg_body = pn.Column(f"Number of classes converted: {role_classes_count}",
                         f"Classes:",
                         role_classes_checkbox_group)

    # msg_body = get_class_cards_from_json("role_classes.json")
    put_class_button = pn.widgets.Button(name="Put", button_type='primary')
    pn.bind(lambda func: put_class_in_domain_model(domain_modeler, role_classes_checkbox_group.value), put_class_button,
            watch=True)
    msg_body.append(pn.Row("Do you wish to put the selected classes in the domain model?", put_class_button))
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def show_roles():
    text_area_input.disabled = True

    user_stories = text_area_input.value
    domain_modeler = DomainModeler(user_stories)

    msg = show_waiting()
    domain_modeler.get_roles()
    remove_waiting(msg)

    class_button = pn.widgets.Button(name="Convert", button_type='primary')
    pn.bind(lambda func: show_role_classes(roles_checkbox_group.value, domain_modeler), class_button,
            watch=True)

    roles_list = domain_modeler.role_list
    roles_checkbox_group = pn.widgets.CheckBoxGroup(name='roles', value=roles_list, options=roles_list,
                                                    inline=False,
                                                    styles={'background': 'WhiteSmoke', 'align': 'Center'})

    msg_body = pn.Column(
        f"Roles Found: {domain_modeler.role_count}",
        "Roles: ",
        roles_checkbox_group,
        pn.Row(f"Do you wish to convert the selected roles in to classes?", class_button),
    )
    message = create_chat_message(msg_body)
    domChat.send(message, respond=False)


def file_input_indicator(event):
    file_input.disabled = True
    text_area_input.value = file_input.value.decode("utf-8")
    role_button = pn.widgets.Button(name="Extract", button_type='primary')
    pn.bind(lambda func: show_roles(), role_button, watch=True)
    msg_body = pn.Column(
        text_area_input,
        pn.Row("Do you wish to extract the roles involved in the user stories", role_button)
    )
    message = create_chat_message(msg_body, user="User", avatar=ChatMessage.default_avatars["human"])
    domChat.send(message, respond=False)


if __name__ == '__main__':
    domChat = ChatInterface(
        # callback=getDomainModel,
        widgets=pn.widgets.TextAreaInput(placeholder="Enter a user story!", auto_grow=True, max_rows=3),
        show_activity_dot=True
    )

    text_area_input = pn.widgets.TextAreaInput(name='User Stories',
                                               placeholder='The selected user stories appear here ...', auto_grow=True)
    file_input = pn.widgets.FileInput()
    pn.bind(file_input_indicator, file_input, watch=True)

    body = pn.Column(
        "I am a domain modeling assistant. Send me the user stories to work out a domain model",
        file_input,
    )

    domChat.send(create_chat_message(body), respond=False)

    pn.extension("perspective")
    dashboard = pn.Column(
        domChat,
    )
    dashboard.show(title="Domain Modeling Prompter")

