n = c(require("crypto-js/sha384")),
l = c(require("crypto-js/enc-base64"));
var f = require("urlsafe-base64");
function c(e) {
    return e && e.__esModule ? e: {
    default:
        e
    }
}

function S(e, t, a) {
    var o = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : 1,
    i = (arguments.length > 4 && arguments[4], arguments.length > 5 && void 0 !== arguments[5] ? arguments[5] : "PC"),
    u = arguments.length > 6 && void 0 !== arguments[6] ? arguments[6] : 1,
    r = ~~ ((new Date).getTime() / 1e3),
    s = "customToken=4c86c01c4f82305f&timestamp=".concat(r, "&phoneNumber=").concat(e),
    d = l.
default.stringify((0, n.
default)(s));
    return {
        tenantId:
        1,
        phoneNumber: e,
        googleCode: t,
        timestamp: r,
        hashCode: f.encode(d),
        sysTemplateCode: o,
        clientType: i,
        clientName: a,
        applicationId: u
    }
};
