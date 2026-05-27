from abc import ABC, abstractmethod

class PedidoRepository(ABC):
    @abstractmethod
    def get_open_pedido(self, usuario_id):
        """Busca o pedido ativo (com status 'ABERTO') do usuário"""
        pass

    @abstractmethod
    def create_open_pedido(self, usuario_id):
        """Cria um novo pedido com status 'ABERTO' para o usuário e retorna o ID gerado"""
        pass

    @abstractmethod
    def add_item_to_pedido(self, pedido_id, item_nome, item_foto, item_valor, quantidade, observacao):
        """Adiciona um item com foto, valor, quantidade e observações ao pedido correspondente"""
        pass

    @abstractmethod
    def get_open_pedido_items(self, usuario_id):
        """Retorna todos os itens do carrinho/pedido aberto do usuário logado"""
        pass

    @abstractmethod
    def delete_item_from_open_pedido(self, pedido_item_id, usuario_id):
        """Remove um item específico do pedido aberto do usuário"""
        pass

    @abstractmethod
    def finalize_open_pedido(self, usuario_id):
        """Marca o pedido aberto atual do usuário como FINALIZADO"""
        pass
