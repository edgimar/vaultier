ApplicationKernel.namespace('Vaultier.dal.mixin');

var decryptedField = Vaultier.dal.mixin.EncryptedModel.decryptedField;

/**
 * @module vaultier-dal-mixin
 * @class Vaultier.dal.mixin.NodeFileMixin
 */
Vaultier.dal.mixin.NodeFileMixin = Ember.Mixin.create({

    /**
     * blob_meta encrypted attrs
     */
    filename: decryptedField('blob_meta', 'filename'),
    filesize: decryptedField('blob_meta', 'filesize'),
    filetype: decryptedField('blob_meta', 'filetype'),

    /**
     * data encrypted attrs
     */
    password: decryptedField('data', 'password'),
    username: decryptedField('data', 'username'),
    url: decryptedField('data', 'url'),
    note: decryptedField('data', 'note'),

    blob: null,

    /**
     * @DI store:main
     */
    store: null,

    init: function () {
        this.set('store', Vaultier.__container__.lookup('store:main'))
        this.on('didLoad', this, this.emptyBlob)
        this.on('didReload', this, this.emptyBlob)
        this.emptyBlob();
    },

    isFile: function () {
        return this.get('type') == this.types['FILE'].value;
    }.property('type'),

    emptyBlob: function () {
        this.set('blob', new Vaultier.dal.model.NodeBlob({
            id: this.get('id')

        }));
        this.set('blob.membership', this.get('membership'));
        Utils.Logger.log.debug(this.get('blob'));
        Utils.Logger.log.debug(this.get('membership'));
    },


    loadBlob: function () {
        var blob = this.get('blob');
        if (!blob.get('isNew')) {
            return Ember.RSVP.resolve(blob)
        } else {
            return this.get('adapter').loadData(this.get('id'))
                .then(function (nodeBlobData) {
                    nodeBlobData.membership = this.get('membership');
                    var nodeBlob = Vaultier.dal.model.NodeBlob.load(nodeBlobData);
                    this.set('blob', nodeBlob);
                    return nodeBlob;
                }.bind(this));
        }
    },

    saveRecord: function () {
        var blob = this.get('blob');
        Utils.Logger.log.debug(blob);
        Utils.Logger.log.debug(this.get('filename'));
        return this
            ._super.apply(this, arguments)
            .then(function () {
                blob.set('id', this.get('id'))
                blob.set('membership', this.get('membership'))
                return blob.saveRecord(this);
            }.bind(this))
            .then(this.emptyBlob.bind(this))
    }
});
